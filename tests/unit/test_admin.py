"""Unit tests for Admin endpoints"""
import pytest


def make_admin(client, auth_headers):
    """Helper: promote current user to admin via DB"""
    from src.core.database import get_db_session
    from src.models.campaign import User
    from flask_jwt_extended import decode_token
    import re
    token = auth_headers['Authorization'].split(' ')[1]
    # Get user from /me endpoint
    res = client.get('/api/v1/auth/me', headers=auth_headers)
    user_id = res.get_json()['user']['id']

    db = get_db_session()
    user = db.query(User).filter_by(id=user_id).first()
    if user:
        user.role = 'admin'
        db.commit()


class TestAdminEndpoints:

    def test_stats_requires_admin(self, client, auth_headers):
        res = client.get('/api/v1/admin/stats', headers=auth_headers)
        assert res.status_code == 403

    def test_stats_requires_auth(self, client):
        res = client.get('/api/v1/admin/stats')
        assert res.status_code == 401

    def test_users_requires_admin(self, client, auth_headers):
        res = client.get('/api/v1/admin/users', headers=auth_headers)
        assert res.status_code == 403
