"""
ADFLOWAI - Admin API Routes
Protected by JWT + admin role check
"""
from functools import wraps
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
import logging

from src.admin.admin_manager import AdminManager
from src.core.database import get_db_session

logger = logging.getLogger(__name__)
admin_bp = Blueprint('admin', __name__, url_prefix='/api/v1/admin')


@admin_bp.route('/bootstrap', methods=['POST'])
@jwt_required()
def bootstrap_admin():
    """
    Make yourself admin - only works if NO admin exists yet.
    This solves the chicken-and-egg problem for first-time setup.
    POST /api/v1/admin/bootstrap  (just needs a valid JWT, no admin role)
    """
    user_id = get_jwt_identity()
    db      = get_db_session()

    # Check if any admin already exists
    from src.models.campaign import User
    existing_admin = db.query(User).filter_by(role='admin').first()
    if existing_admin:
        return jsonify({
            'success': False,
            'error': 'An admin already exists. This endpoint is disabled.'
        }), 403

    # Promote current user to admin
    user = db.query(User).filter_by(id=user_id).first()
    if not user:
        return jsonify({'success': False, 'error': 'User not found'}), 404

    user.role = 'admin'
    db.commit()
    db.refresh(user)

    logger.info(f"Bootstrap: user {user.username} promoted to admin")
    return jsonify({
        'success': True,
        'message': f'{user.username} is now admin! Log out and log back in to see Admin Panel.',
        'user': {'id': user.id, 'username': user.username, 'role': user.role}
    }), 200


def admin_required(fn):
    """Decorator: JWT required + role must be 'admin'"""
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        claims = get_jwt()
        if claims.get('role') != 'admin':
            return jsonify({'success': False, 'error': 'Admin access required'}), 403
        return fn(*args, **kwargs)
    return wrapper


def _mgr():
    return AdminManager(db_session=get_db_session())


# ── System Stats ──────────────────────────────────────────────────────────────

@admin_bp.route('/stats', methods=['GET'])
@admin_required
def system_stats():
    return jsonify({'success': True, 'stats': _mgr().get_system_stats()}), 200


@admin_bp.route('/activity', methods=['GET'])
@admin_required
def recent_activity():
    limit = min(int(request.args.get('limit', 20)), 100)
    return jsonify({'success': True, 'activity': _mgr().get_recent_activity(limit)}), 200


# ── User Management ───────────────────────────────────────────────────────────

@admin_bp.route('/users', methods=['GET'])
@admin_required
def list_users():
    page     = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 20))
    search   = request.args.get('search')
    return jsonify({'success': True, **_mgr().get_all_users(page, per_page, search)}), 200


@admin_bp.route('/users/<int:user_id>', methods=['GET'])
@admin_required
def get_user(user_id):
    mgr  = _mgr()
    user = mgr.get_user(user_id)
    if not user:
        return jsonify({'success': False, 'error': 'User not found'}), 404
    return jsonify({'success': True, 'user': mgr._user_dict(user)}), 200


@admin_bp.route('/users/<int:user_id>', methods=['PUT'])
@admin_required
def update_user(user_id):
    data = request.get_json(silent=True) or {}
    try:
        user = _mgr().update_user(user_id, data)
        return jsonify({'success': True, 'message': 'User updated', 'user': {'id': user.id, 'role': user.role, 'is_active': user.is_active}}), 200
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 404
    except Exception as e:
        logger.error(f"Update user error: {e}")
        return jsonify({'success': False, 'error': 'Update failed'}), 500


@admin_bp.route('/users/<int:user_id>', methods=['DELETE'])
@admin_required
def delete_user(user_id):
    current_id = get_jwt_identity()
    if user_id == current_id:
        return jsonify({'success': False, 'error': 'Cannot delete your own account'}), 400
    try:
        _mgr().delete_user(user_id)
        return jsonify({'success': True, 'message': 'User deleted'}), 200
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 404


@admin_bp.route('/users/<int:user_id>/toggle-active', methods=['POST'])
@admin_required
def toggle_active(user_id):
    current_id = get_jwt_identity()
    if user_id == current_id:
        return jsonify({'success': False, 'error': 'Cannot disable your own account'}), 400
    try:
        user = _mgr().toggle_active(user_id)
        return jsonify({'success': True, 'is_active': user.is_active, 'message': f"User {'activated' if user.is_active else 'deactivated'}"}), 200
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 404


@admin_bp.route('/users/<int:user_id>/role', methods=['POST'])
@admin_required
def set_role(user_id):
    data = request.get_json(silent=True) or {}
    role = data.get('role')
    if not role:
        return jsonify({'success': False, 'error': 'role is required'}), 400
    try:
        user = _mgr().set_role(user_id, role)
        return jsonify({'success': True, 'message': f"Role set to {role}", 'role': user.role}), 200
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
