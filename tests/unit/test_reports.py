"""Unit tests for Report Generator"""
import pytest
from src.reports.report_generator import ReportGenerator


@pytest.fixture
def generator():
    return ReportGenerator()


@pytest.fixture
def sample_campaigns():
    return [
        {
            'id': 1, 'name': 'Campaign A', 'status': 'active',
            'objective': 'conversions', 'total_budget': 5000,
            'spent_budget': 2500, 'impressions': 50000,
            'clicks': 1500, 'conversions': 75,
            'performance_score': 0.78,
            'metrics': {'ctr': 0.03, 'cpc': 1.67, 'cpa': 33.3, 'roas': 3.5},
            'start_date': '2026-01-01T00:00:00', 'created_at': '2025-12-01T00:00:00',
        },
        {
            'id': 2, 'name': 'Campaign B', 'status': 'paused',
            'objective': 'awareness', 'total_budget': 2000,
            'spent_budget': 800, 'impressions': 20000,
            'clicks': 300, 'conversions': 10,
            'performance_score': 0.42,
            'metrics': {'ctr': 0.015, 'cpc': 2.67, 'cpa': 80.0, 'roas': 1.2},
            'start_date': '2026-01-15T00:00:00', 'created_at': '2025-12-15T00:00:00',
        },
    ]


@pytest.fixture
def user_info():
    return {'username': 'testuser', 'company': 'ADFLOWAI Test'}


class TestReportGenerator:

    def test_csv_returns_bytes(self, generator, sample_campaigns, user_info):
        result = generator.generate_csv(sample_campaigns, user_info)
        assert isinstance(result, bytes)
        assert len(result) > 0

    def test_csv_contains_campaign_names(self, generator, sample_campaigns, user_info):
        result = generator.generate_csv(sample_campaigns, user_info).decode('utf-8-sig')
        assert 'Campaign A' in result
        assert 'Campaign B' in result

    def test_csv_contains_headers(self, generator, sample_campaigns, user_info):
        result = generator.generate_csv(sample_campaigns, user_info).decode('utf-8-sig')
        assert 'Total Budget' in result
        assert 'Impressions' in result

    def test_json_returns_bytes(self, generator, sample_campaigns, user_info):
        result = generator.generate_json(sample_campaigns, user_info)
        assert isinstance(result, bytes)

    def test_json_valid_structure(self, generator, sample_campaigns, user_info):
        import json
        result = json.loads(generator.generate_json(sample_campaigns, user_info))
        assert 'report_metadata' in result
        assert 'summary' in result
        assert 'campaigns' in result
        assert result['summary']['total_campaigns'] == 2
        assert result['summary']['total_budget'] == 7000

    def test_html_returns_bytes(self, generator, sample_campaigns, user_info):
        result = generator.generate_html(sample_campaigns, user_info)
        assert isinstance(result, bytes)

    def test_html_contains_campaign_names(self, generator, sample_campaigns, user_info):
        result = generator.generate_html(sample_campaigns, user_info).decode('utf-8')
        assert 'Campaign A' in result
        assert 'Campaign B' in result
        assert 'ADFLOWAI' in result

    def test_empty_campaigns(self, generator, user_info):
        csv_r  = generator.generate_csv([], user_info)
        json_r = generator.generate_json([], user_info)
        html_r = generator.generate_html([], user_info)
        assert isinstance(csv_r, bytes)
        assert isinstance(json_r, bytes)
        assert isinstance(html_r, bytes)
