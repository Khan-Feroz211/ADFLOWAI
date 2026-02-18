"""
ADFLOWAI - Authentication Tests
Tests for user registration, login, and token management
"""

import pytest


class TestAuthentication:
    """Test authentication functionality"""
    
    def test_register_user_success(self, client):
        """Test successful user registration"""
        response = client.post('/api/v1/auth/register', json={
            'username': 'newuser',
            'email': 'newuser@test.com',
            'password': 'SecurePass123!'
        })
        
        assert response.status_code == 201
        data = response.get_json()
        assert data['success'] == True
        assert 'user' in data
        assert 'tokens' in data
        assert data['user']['username'] == 'newuser'
        assert 'access_token' in data['tokens']
    
    def test_register_duplicate_username(self, client):
        """Test registration with duplicate username"""
        # First registration
        client.post('/api/v1/auth/register', json={
            'username': 'duplicate',
            'email': 'user1@test.com',
            'password': 'Pass123!'
        })
        
        # Second registration with same username
        response = client.post('/api/v1/auth/register', json={
            'username': 'duplicate',
            'email': 'user2@test.com',
            'password': 'Pass123!'
        })
        
        assert response.status_code == 400
        data = response.get_json()
        assert 'already exists' in data['error'].lower()
    
    def test_register_weak_password(self, client):
        """Test registration with weak password"""
        response = client.post('/api/v1/auth/register', json={
            'username': 'weakpass',
            'email': 'weak@test.com',
            'password': 'weak'
        })
        
        assert response.status_code == 400
        data = response.get_json()
        assert 'password' in data['error'].lower()
    
    def test_login_success(self, client):
        """Test successful login"""
        # Register first
        client.post('/api/v1/auth/register', json={
            'username': 'logintest',
            'email': 'login@test.com',
            'password': 'LoginPass123!'
        })
        
        # Login
        response = client.post('/api/v1/auth/login', json={
            'username': 'logintest',
            'password': 'LoginPass123!'
        })
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] == True
        assert 'user' in data
        assert 'tokens' in data
    
    def test_login_wrong_password(self, client):
        """Test login with wrong password"""
        # Register first
        client.post('/api/v1/auth/register', json={
            'username': 'wrongpass',
            'email': 'wrong@test.com',
            'password': 'CorrectPass123!'
        })
        
        # Login with wrong password
        response = client.post('/api/v1/auth/login', json={
            'username': 'wrongpass',
            'password': 'WrongPass123!'
        })
        
        assert response.status_code == 401
        data = response.get_json()
        assert data['success'] == False
    
    def test_get_current_user(self, client, auth_headers):
        """Test getting current user info"""
        response = client.get('/api/v1/auth/me', headers=auth_headers)
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] == True
        assert 'user' in data
        assert data['user']['username'].startswith('testuser_')
    
    def test_protected_route_without_token(self, client):
        """Test accessing protected route without token"""
        response = client.get('/api/v1/campaigns')
        
        # Should return 401 unauthorized
        assert response.status_code == 401
