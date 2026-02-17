"""
ADFLOWAI - API Routes
RESTful API endpoints for campaign management
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
import logging

from src.core.campaign_manager import CampaignManager
from src.core.database import get_db_session
from src.auth.auth_routes import auth_bp

logger = logging.getLogger(__name__)

# Create blueprints
api_v1 = Blueprint('api_v1', __name__, url_prefix='/api/v1')


def register_blueprints(app):
    """Register all API blueprints"""
    app.register_blueprint(auth_bp)  # Authentication routes
    app.register_blueprint(api_v1)   # Main API routes
    logger.info("API blueprints registered")


# ============================================================================
# CAMPAIGN ENDPOINTS
# ============================================================================

@api_v1.route('/campaigns', methods=['POST'])
@jwt_required()
def create_campaign():
    """
    Create a new campaign
    
    Request Body:
    {
        "name": "Summer Sale Campaign",
        "total_budget": 10000,
        "platforms": ["google_ads", "facebook", "instagram"],
        "start_date": "2026-03-01T00:00:00",
        "end_date": "2026-03-31T23:59:59",
        "objective": "conversions",
        "target_audience": {
            "age": "25-45",
            "interests": ["technology"],
            "locations": ["US", "CA"]
        },
        "description": "Spring product launch campaign"
    }
    """
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'total_budget', 'platforms', 'start_date']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Parse dates
        start_date = datetime.fromisoformat(data['start_date'].replace('Z', '+00:00'))
        end_date = None
        if 'end_date' in data:
            end_date = datetime.fromisoformat(data['end_date'].replace('Z', '+00:00'))
        
        # Create campaign
        manager = CampaignManager()
        campaign = manager.create_campaign(
            user_id=user_id,
            name=data['name'],
            total_budget=float(data['total_budget']),
            platforms=data['platforms'],
            start_date=start_date,
            end_date=end_date,
            objective=data.get('objective', 'conversions'),
            target_audience=data.get('target_audience'),
            description=data.get('description')
        )
        
        return jsonify({
            'success': True,
            'campaign': campaign.to_dict()
        }), 201
        
    except Exception as e:
        logger.error(f"Error creating campaign: {str(e)}")
        return jsonify({'error': str(e)}), 500


@api_v1.route('/campaigns', methods=['GET'])
@jwt_required()
def get_campaigns():
    """
    Get all campaigns for the authenticated user
    
    Query Parameters:
    - status: Filter by status (active, paused, stopped, completed)
    """
    try:
        user_id = get_jwt_identity()
        status = request.args.get('status')
        
        manager = CampaignManager()
        campaigns = manager.get_user_campaigns(user_id, status)
        
        return jsonify({
            'success': True,
            'count': len(campaigns),
            'campaigns': [c.to_dict() for c in campaigns]
        }), 200
        
    except Exception as e:
        logger.error(f"Error fetching campaigns: {str(e)}")
        return jsonify({'error': str(e)}), 500


@api_v1.route('/campaigns/<int:campaign_id>', methods=['GET'])
@jwt_required()
def get_campaign(campaign_id):
    """Get a specific campaign by ID"""
    try:
        user_id = get_jwt_identity()
        
        manager = CampaignManager()
        campaign = manager.get_campaign(campaign_id)
        
        if not campaign:
            return jsonify({'error': 'Campaign not found'}), 404
        
        if campaign.user_id != user_id:
            return jsonify({'error': 'Unauthorized'}), 403
        
        return jsonify({
            'success': True,
            'campaign': campaign.to_dict()
        }), 200
        
    except Exception as e:
        logger.error(f"Error fetching campaign: {str(e)}")
        return jsonify({'error': str(e)}), 500


@api_v1.route('/campaigns/<int:campaign_id>', methods=['DELETE'])
@jwt_required()
def delete_campaign(campaign_id):
    """Delete a campaign"""
    try:
        user_id = get_jwt_identity()
        
        manager = CampaignManager()
        campaign = manager.get_campaign(campaign_id)
        
        if not campaign:
            return jsonify({'error': 'Campaign not found'}), 404
        
        if campaign.user_id != user_id:
            return jsonify({'error': 'Unauthorized'}), 403
        
        manager.delete_campaign(campaign_id)
        
        return jsonify({
            'success': True,
            'message': 'Campaign deleted successfully'
        }), 200
        
    except Exception as e:
        logger.error(f"Error deleting campaign: {str(e)}")
        return jsonify({'error': str(e)}), 500


@api_v1.route('/campaigns/<int:campaign_id>/metrics', methods=['POST'])
@jwt_required()
def update_campaign_metrics(campaign_id):
    """
    Update campaign metrics
    
    Request Body:
    {
        "impressions": 50000,
        "clicks": 1500,
        "conversions": 75,
        "spent_budget": 2500.00,
        "ctr": 0.03,
        "cpc": 1.67,
        "cpa": 33.33,
        "roas": 3.5
    }
    """
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        manager = CampaignManager()
        campaign = manager.get_campaign(campaign_id)
        
        if not campaign:
            return jsonify({'error': 'Campaign not found'}), 404
        
        if campaign.user_id != user_id:
            return jsonify({'error': 'Unauthorized'}), 403
        
        manager.update_campaign_metrics(campaign_id, metrics=data)
        
        return jsonify({
            'success': True,
            'message': 'Metrics updated successfully'
        }), 200
        
    except Exception as e:
        logger.error(f"Error updating metrics: {str(e)}")
        return jsonify({'error': str(e)}), 500


@api_v1.route('/campaigns/<int:campaign_id>/optimize', methods=['POST'])
@jwt_required()
def optimize_campaign(campaign_id):
    """
    Run AI optimization on a campaign
    
    Returns optimization actions taken
    """
    try:
        user_id = get_jwt_identity()
        
        manager = CampaignManager()
        campaign = manager.get_campaign(campaign_id)
        
        if not campaign:
            return jsonify({'error': 'Campaign not found'}), 404
        
        if campaign.user_id != user_id:
            return jsonify({'error': 'Unauthorized'}), 403
        
        actions = manager.optimize_campaign(campaign_id)
        
        return jsonify({
            'success': True,
            'actions_taken': actions,
            'optimization_timestamp': datetime.utcnow().isoformat()
        }), 200
        
    except Exception as e:
        logger.error(f"Error optimizing campaign: {str(e)}")
        return jsonify({'error': str(e)}), 500


@api_v1.route('/campaigns/<int:campaign_id>/analytics', methods=['GET'])
@jwt_required()
def get_campaign_analytics(campaign_id):
    """Get comprehensive analytics for a campaign"""
    try:
        user_id = get_jwt_identity()
        
        manager = CampaignManager()
        campaign = manager.get_campaign(campaign_id)
        
        if not campaign:
            return jsonify({'error': 'Campaign not found'}), 404
        
        if campaign.user_id != user_id:
            return jsonify({'error': 'Unauthorized'}), 403
        
        analytics = manager.get_campaign_analytics(campaign_id)
        
        return jsonify({
            'success': True,
            'analytics': analytics
        }), 200
        
    except Exception as e:
        logger.error(f"Error fetching analytics: {str(e)}")
        return jsonify({'error': str(e)}), 500


# ============================================================================
# DASHBOARD ENDPOINTS
# ============================================================================

@api_v1.route('/dashboard', methods=['GET'])
@jwt_required()
def get_dashboard():
    """
    Get dashboard overview
    
    Returns summary statistics across all campaigns
    """
    try:
        user_id = get_jwt_identity()
        
        manager = CampaignManager()
        campaigns = manager.get_user_campaigns(user_id)
        
        # Calculate aggregate statistics
        total_budget = sum(c.total_budget for c in campaigns)
        total_spent = sum(c.spent_budget for c in campaigns)
        total_impressions = sum(c.impressions for c in campaigns)
        total_clicks = sum(c.clicks for c in campaigns)
        total_conversions = sum(c.conversions for c in campaigns)
        
        active_campaigns = [c for c in campaigns if c.status.value == 'active']
        paused_campaigns = [c for c in campaigns if c.status.value == 'paused']
        
        avg_performance = sum(c.performance_score for c in campaigns) / len(campaigns) if campaigns else 0
        
        return jsonify({
            'success': True,
            'dashboard': {
                'total_campaigns': len(campaigns),
                'active_campaigns': len(active_campaigns),
                'paused_campaigns': len(paused_campaigns),
                'total_budget': total_budget,
                'total_spent': total_spent,
                'budget_remaining': total_budget - total_spent,
                'total_impressions': total_impressions,
                'total_clicks': total_clicks,
                'total_conversions': total_conversions,
                'avg_ctr': (total_clicks / total_impressions * 100) if total_impressions > 0 else 0,
                'avg_performance_score': avg_performance,
                'top_campaigns': [c.to_dict() for c in sorted(campaigns, key=lambda x: x.performance_score, reverse=True)[:5]]
            }
        }), 200
        
    except Exception as e:
        logger.error(f"Error fetching dashboard: {str(e)}")
        return jsonify({'error': str(e)}), 500


# ============================================================================
# UTILITY ENDPOINTS
# ============================================================================

@api_v1.route('/platforms', methods=['GET'])
def get_supported_platforms():
    """Get list of supported advertising platforms"""
    return jsonify({
        'success': True,
        'platforms': [
            {'id': 'google_ads', 'name': 'Google Ads', 'status': 'active'},
            {'id': 'facebook', 'name': 'Facebook Ads', 'status': 'active'},
            {'id': 'instagram', 'name': 'Instagram Ads', 'status': 'active'},
            {'id': 'linkedin', 'name': 'LinkedIn Ads', 'status': 'active'},
            {'id': 'twitter', 'name': 'Twitter Ads', 'status': 'beta'},
            {'id': 'tiktok', 'name': 'TikTok Ads', 'status': 'beta'}
        ]
    }), 200


@api_v1.route('/health', methods=['GET'])
def health_check():
    """API health check"""
    return jsonify({
        'status': 'healthy',
        'service': 'ADFLOWAI API',
        'version': '1.0.0',
        'timestamp': datetime.utcnow().isoformat()
    }), 200
