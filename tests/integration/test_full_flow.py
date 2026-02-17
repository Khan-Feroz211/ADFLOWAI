"""
Integration tests: full user journey
Register → Login → Create Campaign → Optimize → Get Report
"""
import pytest
from datetime import datetime, timedelta


class TestFullUserJourney:

    def test_register_login_create_campaign(self, client):
        # 1. Register
        reg = client.post('/api/v1/auth/register', json={
            'username': 'journeyuser',
            'email': 'journey@test.com',
            'password': 'JourneyPass123!'
        })
        assert reg.status_code == 201
        token = reg.get_json()['tokens']['access_token']
        headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}

        # 2. Get my profile
        me = client.get('/api/v1/auth/me', headers=headers)
        assert me.status_code == 200
        assert me.get_json()['user']['username'] == 'journeyuser'

        # 3. Create campaign
        camp = client.post('/api/v1/campaigns', json={
            'name': 'Journey Campaign',
            'total_budget': 10000,
            'platforms': ['google_ads', 'facebook'],
            'start_date': datetime.utcnow().isoformat(),
            'end_date': (datetime.utcnow() + timedelta(days=30)).isoformat(),
            'objective': 'conversions',
            'target_audience': {'locations': ['US'], 'age_range': '25-45', 'interests': ['tech']},
        }, headers=headers)
        assert camp.status_code == 201
        campaign_id = camp.get_json()['campaign']['id']

        # 4. View dashboard
        dash = client.get('/api/v1/dashboard', headers=headers)
        assert dash.status_code == 200
        assert dash.get_json()['dashboard']['total_campaigns'] >= 1

        # 5. Update metrics
        metrics = client.post(f'/api/v1/campaigns/{campaign_id}/metrics', json={
            'impressions': 10000, 'clicks': 300, 'conversions': 20,
            'spent_budget': 500, 'ctr': 0.03, 'cpc': 1.67, 'roas': 2.5
        }, headers=headers)
        assert metrics.status_code == 200

        # 6. Run AI optimization
        opt = client.post(f'/api/v1/campaigns/{campaign_id}/optimize', headers=headers)
        assert opt.status_code == 200
        assert opt.get_json()['success'] is True

        # 7. Get report
        report = client.get('/api/v1/reports/campaigns?format=json', headers=headers)
        assert report.status_code == 200
        assert report.content_type == 'application/json'

    def test_report_formats(self, client, auth_headers):
        for fmt in ('csv', 'json', 'html'):
            res = client.get(f'/api/v1/reports/campaigns?format={fmt}', headers=auth_headers)
            assert res.status_code == 200, f"Format {fmt} failed with {res.status_code}"

    def test_platforms_endpoint(self, client):
        res = client.get('/api/v1/platforms')
        assert res.status_code == 200
        data = res.get_json()
        assert data['success'] is True
        assert len(data['platforms']) >= 4
