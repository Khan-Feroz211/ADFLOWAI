# ADFLOWAI - Pytest Configuration

import pytest
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from src.core.database import db
from src.models.campaign import Base
from config.settings import TestingConfig


@pytest.fixture(scope='session')
def app():
    """Create application for testing"""
    app = create_app(TestingConfig)
    
    # Create tables
    with app.app_context():
        db.create_tables()
    
    yield app
    
    # Cleanup
    with app.app_context():
        db.drop_tables()


@pytest.fixture(scope='function')
def client(app):
    """Create test client"""
    return app.test_client()


@pytest.fixture(scope='function')
def db_session(app):
    """Create database session for testing"""
    with app.app_context():
        session = db.get_session()
        yield session
        session.rollback()
        session.close()


@pytest.fixture(scope='function')
def auth_headers(client):
    """Get authentication headers"""
    # Register and login test user
    register_data = {
        'username': 'testuser',
        'email': 'test@test.com',
        'password': 'TestPass123!'
    }
    
    response = client.post('/api/v1/auth/register', json=register_data)
    tokens = response.get_json()['tokens']
    
    return {
        'Authorization': f"Bearer {tokens['access_token']}",
        'Content-Type': 'application/json'
    }
