"""
ADFLOWAI - Report API Routes
Download campaign reports as CSV, JSON, or HTML
"""
from flask import Blueprint, request, jsonify, Response
from flask_jwt_extended import jwt_required, get_jwt_identity
import logging

from src.reports.report_generator import ReportGenerator
from src.core.campaign_manager import CampaignManager
from src.auth.auth_manager import AuthManager
from src.core.database import get_db_session

logger = logging.getLogger(__name__)
reports_bp = Blueprint('reports', __name__, url_prefix='/api/v1/reports')


@reports_bp.route('/campaigns', methods=['GET'])
@jwt_required()
def download_campaign_report():
    """
    GET /api/v1/reports/campaigns?format=csv|json|html
    Downloads a campaign report in the requested format.
    """
    fmt = request.args.get('format', 'csv').lower()
    if fmt not in ('csv', 'json', 'html'):
        return jsonify({'error': "format must be csv, json, or html"}), 400

    user_id = get_jwt_identity()
    db      = get_db_session()

    # Get campaigns
    mgr       = CampaignManager(db_session=db)
    campaigns = mgr.get_user_campaigns(user_id)
    camp_data = [c.to_dict() for c in campaigns]

    # Get user info
    auth      = AuthManager(db_session=db)
    user      = auth.get_user_by_id(user_id)
    user_info = {'username': user.username, 'company': user.company} if user else {}

    # Generate report
    gen = ReportGenerator()
    now = __import__('datetime').datetime.utcnow().strftime('%Y%m%d_%H%M')

    if fmt == 'csv':
        data     = gen.generate_csv(camp_data, user_info)
        mimetype = 'text/csv'
        filename = f'adflowai_campaigns_{now}.csv'

    elif fmt == 'json':
        data     = gen.generate_json(camp_data, user_info)
        mimetype = 'application/json'
        filename = f'adflowai_campaigns_{now}.json'

    else:  # html
        data     = gen.generate_html(camp_data, user_info)
        mimetype = 'text/html'
        filename = f'adflowai_campaigns_{now}.html'

    return Response(
        data,
        mimetype=mimetype,
        headers={'Content-Disposition': f'attachment; filename="{filename}"'}
    )
