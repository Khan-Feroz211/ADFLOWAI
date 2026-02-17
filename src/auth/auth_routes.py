"""
ADFLOWAI - Authentication Routes
All auth endpoints: register, login, refresh, me, change-password, logout
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
    get_jwt,
)
import logging

from src.auth.auth_manager import AuthManager, AuthenticationError
from src.core.database import get_db_session

logger = logging.getLogger(__name__)

auth_bp = Blueprint("auth", __name__, url_prefix="/api/v1/auth")


def _get_manager():
    """Return an AuthManager with a fresh db session."""
    return AuthManager(db_session=get_db_session())


# ── Register ─────────────────────────────────────────────────────────────────

@auth_bp.route("/register", methods=["POST"])
def register():
    """
    POST /api/v1/auth/register
    Body: { username, email, password, full_name?, company? }
    """
    data = request.get_json(silent=True) or {}

    for field in ("username", "email", "password"):
        if not data.get(field):
            return jsonify({"success": False, "error": f"'{field}' is required"}), 400

    try:
        manager = _get_manager()
        user, tokens = manager.register_user(
            username=data["username"],
            email=data["email"],
            password=data["password"],
            full_name=data.get("full_name"),
            company=data.get("company"),
        )
        return jsonify({
            "success": True,
            "user": _user_dict(user),
            "tokens": tokens,
        }), 201

    except AuthenticationError as e:
        return jsonify({"success": False, "error": str(e)}), 400
    except Exception as e:
        logger.error(f"Register error: {e}")
        return jsonify({"success": False, "error": "Registration failed"}), 500


# ── Login ─────────────────────────────────────────────────────────────────────

@auth_bp.route("/login", methods=["POST"])
def login():
    """
    POST /api/v1/auth/login
    Body: { username, password }
    """
    data = request.get_json(silent=True) or {}

    if not data.get("username") or not data.get("password"):
        return jsonify({"success": False, "error": "username and password are required"}), 400

    try:
        manager = _get_manager()
        user, tokens = manager.login(
            username_or_email=data["username"],
            password=data["password"],
        )
        return jsonify({
            "success": True,
            "user": _user_dict(user),
            "tokens": tokens,
        }), 200

    except AuthenticationError as e:
        return jsonify({"success": False, "error": str(e)}), 401
    except Exception as e:
        logger.error(f"Login error: {e}")
        return jsonify({"success": False, "error": "Login failed"}), 500


# ── Refresh ───────────────────────────────────────────────────────────────────

@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    """
    POST /api/v1/auth/refresh
    Header: Authorization: Bearer <refresh_token>
    """
    try:
        user_id = get_jwt_identity()
        manager = _get_manager()
        access_token = manager.refresh_access_token(user_id)
        return jsonify({"success": True, "access_token": access_token}), 200

    except AuthenticationError as e:
        return jsonify({"success": False, "error": str(e)}), 401
    except Exception as e:
        logger.error(f"Refresh error: {e}")
        return jsonify({"success": False, "error": "Token refresh failed"}), 500


# ── Me ────────────────────────────────────────────────────────────────────────

@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def me():
    """
    GET /api/v1/auth/me
    Header: Authorization: Bearer <access_token>
    """
    try:
        user_id = get_jwt_identity()
        manager = _get_manager()
        user = manager.get_user_by_id(user_id)
        if not user:
            return jsonify({"success": False, "error": "User not found"}), 404
        return jsonify({"success": True, "user": _user_dict(user)}), 200

    except Exception as e:
        logger.error(f"Me error: {e}")
        return jsonify({"success": False, "error": "Could not retrieve user"}), 500


# ── Change password ───────────────────────────────────────────────────────────

@auth_bp.route("/change-password", methods=["POST"])
@jwt_required()
def change_password():
    """
    POST /api/v1/auth/change-password
    Body: { old_password, new_password }
    """
    data = request.get_json(silent=True) or {}

    if not data.get("old_password") or not data.get("new_password"):
        return jsonify({"success": False, "error": "old_password and new_password required"}), 400

    try:
        user_id = get_jwt_identity()
        manager = _get_manager()
        manager.change_password(user_id, data["old_password"], data["new_password"])
        return jsonify({"success": True, "message": "Password changed successfully"}), 200

    except AuthenticationError as e:
        return jsonify({"success": False, "error": str(e)}), 400
    except Exception as e:
        logger.error(f"Change password error: {e}")
        return jsonify({"success": False, "error": "Password change failed"}), 500


# ── Logout ────────────────────────────────────────────────────────────────────

@auth_bp.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    """
    POST /api/v1/auth/logout
    (Client should discard tokens - stateless JWT)
    """
    user_id = get_jwt_identity()
    logger.info(f"User {user_id} logged out")
    return jsonify({"success": True, "message": "Logged out successfully"}), 200


# ── Helper ────────────────────────────────────────────────────────────────────

def _user_dict(user) -> dict:
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "full_name": user.full_name,
        "company": user.company,
        "role": user.role,
        "is_verified": user.is_verified,
        "last_login": user.last_login.isoformat() if user.last_login else None,
    }
