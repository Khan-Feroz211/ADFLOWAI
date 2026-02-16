"""
ADFLOWAI - Campaign Manager
Core business logic for campaign management and operations
"""

import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from sqlalchemy.orm import Session

from src.models.campaign import (
    Campaign, PlatformCampaign, MetricsHistory,
    CampaignStatus, Platform, OptimizationLog
)
from src.ml.optimizer import AIOptimizer
from src.core.database import get_db_session

logger = logging.getLogger(__name__)


class CampaignManager:
    """
    Campaign management business logic
    
    Handles:
    - Campaign creation and updates
    - Multi-platform deployment
    - Performance tracking
    - AI-driven optimization
    """
    
    def __init__(self, db_session: Optional[Session] = None):
        """
        Initialize Campaign Manager
        
        Args:
            db_session: Database session (optional)
        """
        self.db = db_session or get_db_session()
        self.ai_optimizer = AIOptimizer()
        
        # Try to load pre-trained models
        try:
            self.ai_optimizer.load_models()
        except:
            logger.info("Using rule-based AI optimization")
    
    def create_campaign(
        self,
        user_id: int,
        name: str,
        total_budget: float,
        platforms: List[str],
        start_date: datetime,
        end_date: Optional[datetime] = None,
        objective: str = "conversions",
        target_audience: Optional[Dict] = None,
        description: Optional[str] = None
    ) -> Campaign:
        """
        Create a new multi-platform campaign
        
        Args:
            user_id: ID of the user creating the campaign
            name: Campaign name
            total_budget: Total budget allocation
            platforms: List of platform names (e.g., ['google_ads', 'facebook'])
            start_date: Campaign start date
            end_date: Campaign end date (optional)
            objective: Campaign objective
            target_audience: Targeting parameters
            description: Campaign description
            
        Returns:
            Created Campaign object
        """
        try:
            # Create main campaign
            campaign = Campaign(
                user_id=user_id,
                name=name,
                description=description,
                total_budget=total_budget,
                remaining_budget=total_budget,
                objective=objective,
                target_audience=target_audience or {},
                start_date=start_date,
                end_date=end_date,
                status=CampaignStatus.DRAFT
            )
            
            self.db.add(campaign)
            self.db.flush()  # Get campaign ID
            
            # Create platform campaigns with initial equal allocation
            platform_budget = total_budget / len(platforms)
            
            for platform_name in platforms:
                try:
                    platform_enum = Platform[platform_name.upper()]
                except KeyError:
                    logger.warning(f"Unknown platform: {platform_name}, skipping")
                    continue
                
                platform_campaign = PlatformCampaign(
                    campaign_id=campaign.id,
                    platform=platform_enum,
                    allocated_budget=platform_budget,
                    is_active=True
                )
                self.db.add(platform_campaign)
            
            self.db.commit()
            logger.info(f"Campaign created: {campaign.id} - {campaign.name}")
            
            return campaign
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error creating campaign: {str(e)}")
            raise
    
    def update_campaign_metrics(
        self,
        campaign_id: int,
        platform: Optional[str] = None,
        metrics: Dict = None
    ) -> None:
        """
        Update campaign performance metrics
        
        Args:
            campaign_id: Campaign ID
            platform: Platform name (optional, for platform-specific updates)
            metrics: Dictionary of metrics to update
        """
        try:
            campaign = self.db.query(Campaign).filter_by(id=campaign_id).first()
            if not campaign:
                raise ValueError(f"Campaign {campaign_id} not found")
            
            # Update main campaign metrics
            if metrics:
                for key, value in metrics.items():
                    if hasattr(campaign, key):
                        setattr(campaign, key, value)
                
                # Recalculate performance score
                campaign_data = {
                    'id': campaign.id,
                    'ctr': campaign.ctr,
                    'cpc': campaign.cpc,
                    'cpa': campaign.cpa,
                    'roas': campaign.roas,
                    'conversion_rate': campaign.conversions / campaign.clicks if campaign.clicks > 0 else 0,
                    'spent_budget': campaign.spent_budget,
                    'total_budget': campaign.total_budget,
                    'impressions': campaign.impressions,
                    'clicks': campaign.clicks,
                    'conversions': campaign.conversions,
                    'start_date': campaign.start_date
                }
                
                campaign.performance_score = self.ai_optimizer.predict_performance(campaign_data)
                campaign.remaining_budget = campaign.total_budget - campaign.spent_budget
                campaign.updated_at = datetime.utcnow()
            
            # Record metrics history
            metrics_record = MetricsHistory(
                campaign_id=campaign_id,
                platform=Platform[platform.upper()] if platform else None,
                impressions=campaign.impressions,
                clicks=campaign.clicks,
                conversions=campaign.conversions,
                spent=campaign.spent_budget,
                ctr=campaign.ctr,
                cpc=campaign.cpc,
                cpa=campaign.cpa,
                roas=campaign.roas,
                performance_score=campaign.performance_score
            )
            self.db.add(metrics_record)
            
            self.db.commit()
            logger.info(f"Metrics updated for campaign {campaign_id}")
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error updating metrics: {str(e)}")
            raise
    
    def optimize_campaign(self, campaign_id: int) -> List[str]:
        """
        Run AI optimization on a campaign
        
        Args:
            campaign_id: Campaign ID
            
        Returns:
            List of actions taken
        """
        actions_taken = []
        
        try:
            campaign = self.db.query(Campaign).filter_by(id=campaign_id).first()
            if not campaign:
                raise ValueError(f"Campaign {campaign_id} not found")
            
            # Get campaign data
            campaign_data = {
                'id': campaign.id,
                'ctr': campaign.ctr,
                'cpc': campaign.cpc,
                'cpa': campaign.cpa,
                'roas': campaign.roas,
                'conversion_rate': campaign.conversions / campaign.clicks if campaign.clicks > 0 else 0,
                'spent_budget': campaign.spent_budget,
                'total_budget': campaign.total_budget,
                'impressions': campaign.impressions,
                'clicks': campaign.clicks,
                'conversions': campaign.conversions,
                'start_date': campaign.start_date
            }
            
            # Get platform data
            platform_data = {}
            for pc in campaign.platform_campaigns:
                platform_data[pc.platform.value] = {
                    'allocated_budget': pc.allocated_budget,
                    'spent_budget': pc.spent_budget,
                    'performance_score': pc.performance_score,
                    'is_active': pc.is_active
                }
            
            # Get historical data
            history_records = self.db.query(MetricsHistory)\
                .filter_by(campaign_id=campaign_id)\
                .order_by(MetricsHistory.recorded_at.desc())\
                .limit(30)\
                .all()
            
            history = [{
                'ctr': h.ctr,
                'cpc': h.cpc,
                'cpa': h.cpa,
                'roas': h.roas,
                'performance_score': h.performance_score
            } for h in history_records]
            
            # Get AI recommendations
            recommendations = self.ai_optimizer.get_recommendations(
                campaign_data,
                platform_data,
                history
            )
            
            # Execute recommendations
            for rec in recommendations:
                action_result = self._execute_recommendation(campaign, rec)
                actions_taken.append(action_result)
            
            # Update optimization timestamp
            campaign.last_optimization = datetime.utcnow()
            self.db.commit()
            
            logger.info(f"Optimization completed for campaign {campaign_id}: {len(actions_taken)} actions")
            return actions_taken
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error optimizing campaign: {str(e)}")
            raise
    
    def _execute_recommendation(self, campaign: Campaign, recommendation) -> str:
        """
        Execute an optimization recommendation
        
        Args:
            campaign: Campaign object
            recommendation: OptimizationRecommendation object
            
        Returns:
            Description of action taken
        """
        action = recommendation.action
        
        # Log the optimization action
        log_entry = OptimizationLog(
            campaign_id=campaign.id,
            action=action,
            reason=recommendation.reason,
            confidence_score=recommendation.confidence,
            before_state={'budget': campaign.total_budget, 'status': campaign.status.value}
        )
        
        try:
            if action == 'pause':
                campaign.status = CampaignStatus.PAUSED
                result = f"Campaign paused: {recommendation.reason}"
                
            elif action == 'increase_budget':
                old_budget = campaign.total_budget
                campaign.total_budget = recommendation.suggested_budget
                campaign.remaining_budget = campaign.total_budget - campaign.spent_budget
                result = f"Budget increased from ${old_budget:.2f} to ${campaign.total_budget:.2f}"
                
            elif action == 'decrease_budget':
                old_budget = campaign.total_budget
                campaign.total_budget = recommendation.suggested_budget
                campaign.remaining_budget = campaign.total_budget - campaign.spent_budget
                result = f"Budget decreased from ${old_budget:.2f} to ${campaign.total_budget:.2f}"
                
            elif action == 'reallocate':
                # Reallocate budgets across platforms
                for platform_name, new_budget in recommendation.platform_allocations.items():
                    platform_campaign = self.db.query(PlatformCampaign)\
                        .filter_by(campaign_id=campaign.id)\
                        .filter_by(platform=Platform[platform_name.upper()])\
                        .first()
                    
                    if platform_campaign:
                        platform_campaign.allocated_budget = new_budget
                
                result = f"Budget reallocated across platforms"
                
            else:
                result = f"Unknown action: {action}"
            
            log_entry.after_state = {'budget': campaign.total_budget, 'status': campaign.status.value}
            log_entry.success = True
            self.db.add(log_entry)
            
            return result
            
        except Exception as e:
            log_entry.success = False
            log_entry.error_message = str(e)
            self.db.add(log_entry)
            logger.error(f"Error executing recommendation: {str(e)}")
            return f"Failed to execute {action}: {str(e)}"
    
    def get_campaign(self, campaign_id: int) -> Optional[Campaign]:
        """Get campaign by ID"""
        return self.db.query(Campaign).filter_by(id=campaign_id).first()
    
    def get_user_campaigns(self, user_id: int, status: Optional[str] = None) -> List[Campaign]:
        """
        Get all campaigns for a user
        
        Args:
            user_id: User ID
            status: Optional status filter
            
        Returns:
            List of Campaign objects
        """
        query = self.db.query(Campaign).filter_by(user_id=user_id)
        
        if status:
            try:
                status_enum = CampaignStatus[status.upper()]
                query = query.filter_by(status=status_enum)
            except KeyError:
                logger.warning(f"Invalid status filter: {status}")
        
        return query.order_by(Campaign.created_at.desc()).all()
    
    def delete_campaign(self, campaign_id: int) -> bool:
        """
        Delete a campaign
        
        Args:
            campaign_id: Campaign ID
            
        Returns:
            True if deleted, False otherwise
        """
        try:
            campaign = self.db.query(Campaign).filter_by(id=campaign_id).first()
            if campaign:
                self.db.delete(campaign)
                self.db.commit()
                logger.info(f"Campaign {campaign_id} deleted")
                return True
            return False
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error deleting campaign: {str(e)}")
            raise
    
    def get_campaign_analytics(self, campaign_id: int) -> Dict:
        """
        Get comprehensive analytics for a campaign
        
        Args:
            campaign_id: Campaign ID
            
        Returns:
            Dictionary with analytics data
        """
        campaign = self.get_campaign(campaign_id)
        if not campaign:
            raise ValueError(f"Campaign {campaign_id} not found")
        
        # Get platform breakdown
        platform_breakdown = []
        for pc in campaign.platform_campaigns:
            platform_breakdown.append({
                'platform': pc.platform.value,
                'allocated_budget': pc.allocated_budget,
                'spent_budget': pc.spent_budget,
                'performance_score': pc.performance_score,
                'is_active': pc.is_active
            })
        
        # Get historical trends
        history = self.db.query(MetricsHistory)\
            .filter_by(campaign_id=campaign_id)\
            .order_by(MetricsHistory.recorded_at)\
            .all()
        
        trends = [{
            'timestamp': h.recorded_at.isoformat(),
            'impressions': h.impressions,
            'clicks': h.clicks,
            'conversions': h.conversions,
            'spent': h.spent,
            'performance_score': h.performance_score
        } for h in history]
        
        return {
            'campaign': campaign.to_dict(),
            'platforms': platform_breakdown,
            'trends': trends,
            'summary': {
                'total_impressions': campaign.impressions,
                'total_clicks': campaign.clicks,
                'total_conversions': campaign.conversions,
                'total_spent': campaign.spent_budget,
                'budget_remaining': campaign.remaining_budget,
                'performance_score': campaign.performance_score,
                'roi': ((campaign.conversions * campaign.cpa) - campaign.spent_budget) / campaign.spent_budget if campaign.spent_budget > 0 else 0
            }
        }
