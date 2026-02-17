#!/usr/bin/env python
"""
ADFLOWAI - Database Initialization Script
Creates all tables and optionally seeds test data
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.models.campaign import Base
from src.core.database import db
from config.settings import Config
from src.auth.auth_manager import AuthManager
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init_database(seed_data=False):
    """
    Initialize database
    
    Args:
        seed_data: If True, create test user and sample data
    """
    try:
        logger.info("Initializing database...")
        
        # Create all tables
        db.create_tables()
        logger.info("✓ Database tables created")
        
        if seed_data:
            logger.info("Seeding test data...")
            seed_test_data()
            logger.info("✓ Test data seeded")
        
        logger.info("Database initialization complete!")
        
    except Exception as e:
        logger.error(f"Error initializing database: {str(e)}")
        raise


def seed_test_data():
    """Create test user and sample campaigns"""
    from src.core.campaign_manager import CampaignManager
    from datetime import datetime, timedelta
    
    try:
        # Create test user
        auth_manager = AuthManager()
        
        try:
            user, tokens = auth_manager.register_user(
                username="testuser",
                email="test@adflowai.com",
                password="TestPass123!",
                full_name="Test User",
                company="ADFLOWAI Demo"
            )
            logger.info(f"✓ Test user created: testuser / TestPass123!")
            logger.info(f"  Access token: {tokens['access_token'][:50]}...")
            
        except Exception as e:
            if "already exists" in str(e):
                logger.info("Test user already exists")
                # Login to get user
                user, tokens = auth_manager.login("testuser", "TestPass123!")
            else:
                raise
        
        # Create sample campaigns
        campaign_manager = CampaignManager()
        
        # Campaign 1: Active high-performer
        try:
            campaign1 = campaign_manager.create_campaign(
                user_id=user.id,
                name="Summer Product Launch",
                total_budget=10000.00,
                platforms=["google_ads", "facebook"],
                start_date=datetime.now(),
                end_date=datetime.now() + timedelta(days=30),
                objective="conversions",
                target_audience={
                    "age_range": "25-45",
                    "interests": ["technology", "gadgets"],
                    "locations": ["US", "UK", "CA"]
                },
                description="Major product launch for Q2"
            )
            
            # Add some metrics
            campaign_manager.update_campaign_metrics(
                campaign_id=campaign1.id,
                metrics={
                    'impressions': 50000,
                    'clicks': 1500,
                    'conversions': 75,
                    'spent_budget': 2500.00,
                    'ctr': 0.03,
                    'cpc': 1.67,
                    'cpa': 33.33,
                    'roas': 3.5
                }
            )
            
            logger.info(f"✓ Sample campaign 1 created: {campaign1.name}")
            
        except Exception as e:
            logger.warning(f"Campaign 1 creation skipped: {str(e)}")
        
        # Campaign 2: Underperforming
        try:
            campaign2 = campaign_manager.create_campaign(
                user_id=user.id,
                name="Brand Awareness Campaign",
                total_budget=5000.00,
                platforms=["instagram", "facebook"],
                start_date=datetime.now() - timedelta(days=7),
                end_date=datetime.now() + timedelta(days=23),
                objective="awareness",
                target_audience={
                    "age_range": "18-35",
                    "interests": ["fashion", "lifestyle"],
                    "locations": ["US"]
                }
            )
            
            campaign_manager.update_campaign_metrics(
                campaign_id=campaign2.id,
                metrics={
                    'impressions': 30000,
                    'clicks': 300,
                    'conversions': 5,
                    'spent_budget': 1500.00,
                    'ctr': 0.01,
                    'cpc': 5.00,
                    'cpa': 300.00,
                    'roas': 0.5
                }
            )
            
            logger.info(f"✓ Sample campaign 2 created: {campaign2.name}")
            
        except Exception as e:
            logger.warning(f"Campaign 2 creation skipped: {str(e)}")
        
        logger.info("\n" + "="*60)
        logger.info("TEST CREDENTIALS:")
        logger.info("  Username: testuser")
        logger.info("  Password: TestPass123!")
        logger.info("  Email: test@adflowai.com")
        logger.info("="*60 + "\n")
        
    except Exception as e:
        logger.error(f"Error seeding test data: {str(e)}")
        raise


def drop_all_tables():
    """Drop all tables (USE WITH CAUTION!)"""
    confirm = input("Are you sure you want to DROP ALL TABLES? (yes/no): ")
    if confirm.lower() == 'yes':
        db.drop_tables()
        logger.info("All tables dropped")
    else:
        logger.info("Operation cancelled")


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Initialize ADFLOWAI database')
    parser.add_argument('--seed', action='store_true', help='Seed test data')
    parser.add_argument('--drop', action='store_true', help='Drop all tables (DANGEROUS!)')
    
    args = parser.parse_args()
    
    if args.drop:
        drop_all_tables()
    else:
        # Initialize Flask app context
        from app import app
        with app.app_context():
            init_database(seed_data=args.seed)
