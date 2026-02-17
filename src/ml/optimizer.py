"""
ADFLOWAI - AI Optimization Engine
Machine Learning models for campaign performance prediction and optimization
"""

import logging
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass

from sklearn.ensemble import RandomForestRegressor, GradientBoostingClassifier
from sklearn.preprocessing import StandardScaler
import joblib

logger = logging.getLogger(__name__)


@dataclass
class OptimizationRecommendation:
    """Recommendation from AI optimization"""
    campaign_id: int
    action: str  # 'increase_budget', 'decrease_budget', 'pause', 'resume', 'reallocate'
    confidence: float
    reason: str
    suggested_budget: Optional[float] = None
    platform_allocations: Optional[Dict[str, float]] = None


class AIOptimizer:
    """
    AI-powered campaign optimization engine
    
    Uses machine learning to:
    - Predict campaign performance
    - Recommend budget allocations
    - Identify underperforming campaigns
    - Optimize cross-platform spending
    """
    
    def __init__(self, model_path='models/'):
        """
        Initialize AI Optimizer
        
        Args:
            model_path: Path to saved ML models
        """
        self.model_path = model_path
        self.performance_model = None
        self.pause_classifier = None
        self.scaler = StandardScaler()
        
        # Thresholds (can be configured)
        self.high_performance_threshold = 0.8
        self.low_performance_threshold = 0.3
        self.min_data_points = 10
        
        logger.info("AI Optimizer initialized")
    
    def predict_performance(self, campaign_data: Dict) -> float:
        """
        Predict campaign performance score (0-1)
        
        Args:
            campaign_data: Dictionary with campaign metrics
            
        Returns:
            Performance score between 0 and 1
        """
        try:
            features = self._extract_features(campaign_data)
            
            if self.performance_model is None:
                # Use rule-based prediction if no trained model
                return self._rule_based_performance(campaign_data)
            
            # ML-based prediction
            features_scaled = self.scaler.transform([features])
            score = self.performance_model.predict(features_scaled)[0]
            
            # Ensure score is between 0 and 1
            return max(0.0, min(1.0, score))
            
        except Exception as e:
            logger.error(f"Error predicting performance: {str(e)}")
            return 0.5  # Default neutral score
    
    def _rule_based_performance(self, campaign_data: Dict) -> float:
        """
        Rule-based performance calculation when ML model is not available
        
        Args:
            campaign_data: Campaign metrics
            
        Returns:
            Performance score
        """
        score = 0.5  # Start with neutral
        
        # CTR contribution (30%)
        ctr = campaign_data.get('ctr', 0)
        if ctr > 0.03:  # >3% is excellent
            score += 0.15
        elif ctr > 0.02:  # >2% is good
            score += 0.10
        elif ctr > 0.01:  # >1% is average
            score += 0.05
        elif ctr < 0.005:  # <0.5% is poor
            score -= 0.15
        
        # ROAS contribution (40%)
        roas = campaign_data.get('roas', 0)
        if roas > 4.0:  # 4x return is excellent
            score += 0.20
        elif roas > 3.0:  # 3x is good
            score += 0.15
        elif roas > 2.0:  # 2x is acceptable
            score += 0.10
        elif roas < 1.0:  # Below break-even
            score -= 0.20
        
        # Conversion rate contribution (20%)
        conversion_rate = campaign_data.get('conversion_rate', 0)
        if conversion_rate > 0.05:  # >5% is excellent
            score += 0.10
        elif conversion_rate > 0.03:  # >3% is good
            score += 0.05
        elif conversion_rate < 0.01:  # <1% is poor
            score -= 0.10
        
        # Budget efficiency contribution (10%)
        budget_used_ratio = campaign_data.get('spent_budget', 0) / campaign_data.get('total_budget', 1)
        if 0.3 <= budget_used_ratio <= 0.8:  # Healthy spending rate
            score += 0.05
        elif budget_used_ratio > 0.95:  # Burning budget too fast
            score -= 0.05
        
        return max(0.0, min(1.0, score))
    
    def should_pause_campaign(self, campaign_data: Dict, history: List[Dict]) -> Tuple[bool, str]:
        """
        Determine if a campaign should be paused
        
        Args:
            campaign_data: Current campaign data
            history: Historical performance data
            
        Returns:
            Tuple of (should_pause, reason)
        """
        # Need sufficient data
        if len(history) < self.min_data_points:
            return False, "Insufficient data for decision"
        
        performance_score = self.predict_performance(campaign_data)
        
        # Low performance check
        if performance_score < self.low_performance_threshold:
            return True, f"Low performance score: {performance_score:.2f}"
        
        # Declining trend check
        recent_scores = [self.predict_performance(h) for h in history[-7:]]  # Last 7 data points
        if len(recent_scores) >= 3:
            trend = np.polyfit(range(len(recent_scores)), recent_scores, 1)[0]
            if trend < -0.05:  # Declining trend
                return True, f"Declining performance trend: {trend:.3f}"
        
        # Budget burn without results
        spent_ratio = campaign_data.get('spent_budget', 0) / campaign_data.get('total_budget', 1)
        conversions = campaign_data.get('conversions', 0)
        if spent_ratio > 0.5 and conversions == 0:
            return True, "High spend with zero conversions"
        
        # CPA too high
        cpa = campaign_data.get('cpa', 0)
        target_cpa = campaign_data.get('target_cpa', float('inf'))
        if cpa > target_cpa * 2:  # CPA is 2x target
            return True, f"CPA (${cpa:.2f}) exceeds 2x target (${target_cpa:.2f})"
        
        return False, "Campaign performing adequately"
    
    def optimize_budget_allocation(
        self, 
        campaign_budget: float,
        platform_performances: Dict[str, Dict]
    ) -> Dict[str, float]:
        """
        Optimize budget allocation across platforms based on performance
        
        Args:
            campaign_budget: Total campaign budget
            platform_performances: Dict mapping platform to performance metrics
            
        Returns:
            Dict mapping platform to allocated budget
        """
        allocations = {}
        
        # Calculate performance scores for each platform
        platform_scores = {}
        for platform, metrics in platform_performances.items():
            score = self.predict_performance(metrics)
            platform_scores[platform] = score
        
        # Ensure minimum allocation (10%) for each platform to allow testing
        min_allocation = 0.10
        num_platforms = len(platform_scores)
        remaining_budget = campaign_budget * (1 - (min_allocation * num_platforms))
        
        # Allocate minimum to all
        for platform in platform_scores:
            allocations[platform] = campaign_budget * min_allocation
        
        # Distribute remaining based on performance scores
        total_score = sum(platform_scores.values())
        
        if total_score > 0:
            for platform, score in platform_scores.items():
                additional = (score / total_score) * remaining_budget
                allocations[platform] += additional
        else:
            # Equal distribution if no clear winner
            equal_share = remaining_budget / num_platforms
            for platform in allocations:
                allocations[platform] += equal_share
        
        return allocations
    
    def get_recommendations(
        self,
        campaign_data: Dict,
        platform_data: Dict[str, Dict],
        history: List[Dict]
    ) -> List[OptimizationRecommendation]:
        """
        Generate optimization recommendations for a campaign
        
        Args:
            campaign_data: Main campaign data
            platform_data: Platform-specific performance data
            history: Historical performance data
            
        Returns:
            List of optimization recommendations
        """
        recommendations = []
        
        # Overall performance check
        performance_score = self.predict_performance(campaign_data)
        
        # Check if campaign should be paused
        should_pause, pause_reason = self.should_pause_campaign(campaign_data, history)
        if should_pause:
            recommendations.append(OptimizationRecommendation(
                campaign_id=campaign_data['id'],
                action='pause',
                confidence=0.9,
                reason=pause_reason
            ))
            return recommendations  # Critical action, return immediately
        
        # Budget optimization recommendations
        current_budget = campaign_data.get('total_budget', 0)
        spent_ratio = campaign_data.get('spent_budget', 0) / current_budget if current_budget > 0 else 0
        
        if performance_score > self.high_performance_threshold:
            # High performing campaign - consider increasing budget
            suggested_increase = min(current_budget * 0.5, current_budget * 1.5)  # Max 50% increase
            recommendations.append(OptimizationRecommendation(
                campaign_id=campaign_data['id'],
                action='increase_budget',
                confidence=performance_score,
                reason=f"High performance score ({performance_score:.2f}) indicates room for growth",
                suggested_budget=current_budget + suggested_increase
            ))
        elif performance_score < 0.5 and spent_ratio > 0.3:
            # Underperforming with significant spend
            suggested_decrease = current_budget * 0.3  # Reduce by 30%
            recommendations.append(OptimizationRecommendation(
                campaign_id=campaign_data['id'],
                action='decrease_budget',
                confidence=0.8,
                reason=f"Underperforming ({performance_score:.2f}) with {spent_ratio*100:.1f}% budget spent",
                suggested_budget=current_budget - suggested_decrease
            ))
        
        # Platform reallocation recommendations
        if len(platform_data) > 1:
            optimal_allocation = self.optimize_budget_allocation(
                current_budget,
                platform_data
            )
            
            # Check if reallocation is significantly different
            current_allocation = {p: d.get('allocated_budget', 0) for p, d in platform_data.items()}
            max_diff = max(
                abs(optimal_allocation.get(p, 0) - current_allocation.get(p, 0))
                for p in current_allocation
            )
            
            if max_diff > current_budget * 0.15:  # >15% difference
                recommendations.append(OptimizationRecommendation(
                    campaign_id=campaign_data['id'],
                    action='reallocate',
                    confidence=0.85,
                    reason="Significant performance differences detected across platforms",
                    platform_allocations=optimal_allocation
                ))
        
        return recommendations
    
    def _extract_features(self, campaign_data: Dict) -> List[float]:
        """
        Extract features from campaign data for ML models
        
        Args:
            campaign_data: Campaign metrics dictionary
            
        Returns:
            List of feature values
        """
        return [
            campaign_data.get('ctr', 0),
            campaign_data.get('cpc', 0),
            campaign_data.get('cpa', 0),
            campaign_data.get('roas', 0),
            campaign_data.get('conversion_rate', 0),
            campaign_data.get('spent_budget', 0) / campaign_data.get('total_budget', 1),
            campaign_data.get('impressions', 0),
            campaign_data.get('clicks', 0),
            campaign_data.get('conversions', 0),
            (datetime.utcnow() - campaign_data.get('start_date', datetime.utcnow())).days
        ]
    
    def train_models(self, training_data: List[Dict], labels: List[float]):
        """
        Train ML models on historical data
        
        Args:
            training_data: List of campaign data dictionaries
            labels: Performance scores or outcomes
        """
        try:
            # Extract features
            X = np.array([self._extract_features(data) for data in training_data])
            y = np.array(labels)
            
            # Scale features
            X_scaled = self.scaler.fit_transform(X)
            
            # Train performance prediction model
            self.performance_model = RandomForestRegressor(
                n_estimators=100,
                max_depth=10,
                random_state=42
            )
            self.performance_model.fit(X_scaled, y)
            
            # Save models
            joblib.dump(self.performance_model, f"{self.model_path}performance_model.pkl")
            joblib.dump(self.scaler, f"{self.model_path}scaler.pkl")
            
            logger.info("ML models trained successfully")
            
        except Exception as e:
            logger.error(f"Error training models: {str(e)}")
            raise
    
    def load_models(self):
        """Load pre-trained models from disk"""
        try:
            self.performance_model = joblib.load(f"{self.model_path}performance_model.pkl")
            self.scaler = joblib.load(f"{self.model_path}scaler.pkl")
            logger.info("ML models loaded successfully")
        except FileNotFoundError:
            logger.warning("Pre-trained models not found. Using rule-based predictions.")
        except Exception as e:
            logger.error(f"Error loading models: {str(e)}")
