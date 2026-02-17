"""
ADFLOWAI - Test Configuration
Shared fixtures for all tests
"""
import pytest
import os

# Force SQLite for all tests - no Postgres needed
os.environ.setdefault('DATABASE_URL', 'sqlite:///:memory:')
os.environ.setdefault('SECRET_KEY', 'test-secret-key')
os.environ.setdefault('JWT_SECRET_KEY', 'test-jwt-secret')
os.environ.setdefault('REDIS_URL', 'redis://localhost:6379/0')


@pytest.fixture(scope='session')
def app():
    """Create a test Flask app with SQLite in-memory database."""
    from config.settings import TestingConfig
    from app import create_app

    TestingConfig.SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    test_app = create_app(TestingConfig)
    test_app.config['TESTING'] = True
    test_app.config['WTF_CSRF_ENABLED'] = False

    with test_app.app_context():
        yield test_app


@pytest.fixture(scope='function')
def client(app):
    """Test client - fresh per test function."""
    return app.test_client()


@pytest.fixture(scope='function')
def auth_headers(client):
    """
    Register a test user and return auth headers.
    Uses a unique username per test to avoid conflicts.
    """
    import uuid
    unique = uuid.uuid4().hex[:8]

    reg = client.post('/api/v1/auth/register', json={
        'username': f'testuser_{unique}',
        'email':    f'test_{unique}@adflowai.com',
        'password': 'TestPass123!',
    })

    assert reg.status_code == 201, f"Registration failed: {reg.get_json()}"
    token = reg.get_json()['tokens']['access_token']

    return {
        'Authorization':  f'Bearer {token}',
        'Content-Type':   'application/json',
    }
