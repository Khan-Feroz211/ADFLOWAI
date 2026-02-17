"""Unit tests for CampaignManager"""
import pytest
from datetime import datetime, timedelta
from unittest.mock import MagicMock, patch


class TestCampaignCreation:

    def test_create_campaign_success(self, client, auth_headers):
        payload = {
            'name': 'Test Campaign',
            'total_budget': 5000,
            'platforms': ['google_ads', 'facebook'],
            'start_date': (datetime.utcnow() + timedelta(days=1)).isoformat(),
            'objective': 'conversions',
        }
        res = client.post('/api/v1/campaigns', json=payload, headers=auth_headers)
        assert res.status_code == 201
        data = res.get_json()
        assert data['success'] is True
        assert data['campaign']['name'] == 'Test Campaign'
        assert data['campaign']['total_budget'] == 5000

    def test_create_campaign_missing_name(self, client, auth_headers):
        payload = {'total_budget': 1000, 'platforms': ['google_ads'], 'start_date': datetime.utcnow().isoformat()}
        res = client.post('/api/v1/campaigns', json=payload, headers=auth_headers)
        assert res.status_code == 400

    def test_create_campaign_missing_budget(self, client, auth_headers):
        payload = {'name': 'No Budget', 'platforms': ['google_ads'], 'start_date': datetime.utcnow().isoformat()}
        res = client.post('/api/v1/campaigns', json=payload, headers=auth_headers)
        assert res.status_code == 400

    def test_create_campaign_requires_auth(self, client):
        res = client.post('/api/v1/campaigns', json={'name': 'Test'})
        assert res.status_code == 401

    def test_list_campaigns_empty(self, client, auth_headers):
        res = client.get('/api/v1/campaigns', headers=auth_headers)
        assert res.status_code == 200
        data = res.get_json()
        assert data['success'] is True
        assert isinstance(data['campaigns'], list)

    def test_create_and_list_campaign(self, client, auth_headers):
        # Create
        payload = {
            'name': 'List Test',
            'total_budget': 2000,
            'platforms': ['google_ads'],
            'start_date': datetime.utcnow().isoformat(),
        }
        client.post('/api/v1/campaigns', json=payload, headers=auth_headers)

        # List
        res = client.get('/api/v1/campaigns', headers=auth_headers)
        assert res.status_code == 200
        assert res.get_json()['count'] >= 1

    def test_get_campaign_by_id(self, client, auth_headers):
        # Create first
        payload = {'name': 'Get Test', 'total_budget': 1000, 'platforms': ['facebook'], 'start_date': datetime.utcnow().isoformat()}
        create_res = client.post('/api/v1/campaigns', json=payload, headers=auth_headers)
        campaign_id = create_res.get_json()['campaign']['id']

        # Get by ID
        res = client.get(f'/api/v1/campaigns/{campaign_id}', headers=auth_headers)
        assert res.status_code == 200
        assert res.get_json()['campaign']['id'] == campaign_id

    def test_get_nonexistent_campaign(self, client, auth_headers):
        res = client.get('/api/v1/campaigns/99999', headers=auth_headers)
        assert res.status_code == 404

    def test_delete_campaign(self, client, auth_headers):
        payload = {'name': 'Delete Me', 'total_budget': 500, 'platforms': ['instagram'], 'start_date': datetime.utcnow().isoformat()}
        create_res = client.post('/api/v1/campaigns', json=payload, headers=auth_headers)
        campaign_id = create_res.get_json()['campaign']['id']

        del_res = client.delete(f'/api/v1/campaigns/{campaign_id}', headers=auth_headers)
        assert del_res.status_code == 200

        get_res = client.get(f'/api/v1/campaigns/{campaign_id}', headers=auth_headers)
        assert get_res.status_code == 404

    def test_optimize_campaign(self, client, auth_headers):
        payload = {'name': 'Optimize Me', 'total_budget': 3000, 'platforms': ['google_ads'], 'start_date': datetime.utcnow().isoformat()}
        create_res = client.post('/api/v1/campaigns', json=payload, headers=auth_headers)
        campaign_id = create_res.get_json()['campaign']['id']

        opt_res = client.post(f'/api/v1/campaigns/{campaign_id}/optimize', headers=auth_headers)
        assert opt_res.status_code == 200
        data = opt_res.get_json()
        assert data['success'] is True
        assert 'actions_taken' in data
