"""
ADFLOWAI Configuration Settings
Centralized configuration management
"""

import os
from datetime import timedelta


class Config:
    """Base configuration"""
    
    # Application Settings
    APP_NAME = os.getenv('APP_NAME', 'ADFLOWAI')
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')
    
    # Database Configuration
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'sqlite:///adflowai_dev.db'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_POOL_SIZE = int(os.getenv('DATABASE_POOL_SIZE', 20))
    SQLALCHEMY_MAX_OVERFLOW = int(os.getenv('DATABASE_MAX_OVERFLOW', 10))
    SQLALCHEMY_POOL_TIMEOUT = int(os.getenv('DATABASE_POOL_TIMEOUT', 30))
    
    # Redis Configuration
    REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
    REDIS_CACHE_TTL = int(os.getenv('REDIS_CACHE_TTL', 3600))
    
    # JWT Configuration
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt-secret-change-in-production')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(
        seconds=int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES', 3600))
    )
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(
        seconds=int(os.getenv('JWT_REFRESH_TOKEN_EXPIRES', 2592000))
    )
    
    # CORS Settings
    CORS_ORIGINS = os.getenv(
        'CORS_ORIGINS',
        'http://localhost:3000,http://localhost:5000'
    ).split(',')
    
    # API Rate Limiting
    API_RATE_LIMIT = int(os.getenv('API_RATE_LIMIT', 100))
    
    # Platform API Keys - Google Ads
    GOOGLE_ADS_DEVELOPER_TOKEN = os.getenv('GOOGLE_ADS_DEVELOPER_TOKEN', '')
    GOOGLE_ADS_CLIENT_ID = os.getenv('GOOGLE_ADS_CLIENT_ID', '')
    GOOGLE_ADS_CLIENT_SECRET = os.getenv('GOOGLE_ADS_CLIENT_SECRET', '')
    GOOGLE_ADS_REFRESH_TOKEN = os.getenv('GOOGLE_ADS_REFRESH_TOKEN', '')
    
    # Platform API Keys - Facebook/Instagram
    FACEBOOK_APP_ID = os.getenv('FACEBOOK_APP_ID', '')
    FACEBOOK_APP_SECRET = os.getenv('FACEBOOK_APP_SECRET', '')
    FACEBOOK_ACCESS_TOKEN = os.getenv('FACEBOOK_ACCESS_TOKEN', '')
    
    # Platform API Keys - LinkedIn
    LINKEDIN_CLIENT_ID = os.getenv('LINKEDIN_CLIENT_ID', '')
    LINKEDIN_CLIENT_SECRET = os.getenv('LINKEDIN_CLIENT_SECRET', '')
    LINKEDIN_ACCESS_TOKEN = os.getenv('LINKEDIN_ACCESS_TOKEN', '')
    
    # ML/AI Configuration
    ML_MODEL_PATH = os.getenv('ML_MODEL_PATH', 'models/')
    ML_PREDICTION_CONFIDENCE_THRESHOLD = float(
        os.getenv('ML_PREDICTION_CONFIDENCE_THRESHOLD', 0.75)
    )
    AUTO_PAUSE_THRESHOLD = float(os.getenv('AUTO_PAUSE_THRESHOLD', 0.3))
    AUTO_REALLOCATE = os.getenv('AUTO_REALLOCATE', 'True').lower() == 'true'
    
    # Campaign Optimization Settings
    OPTIMIZATION_CHECK_INTERVAL = int(os.getenv('OPTIMIZATION_CHECK_INTERVAL', 3600))
    MIN_BUDGET_THRESHOLD = float(os.getenv('MIN_BUDGET_THRESHOLD', 100))
    MAX_BUDGET_INCREASE_PERCENT = int(os.getenv('MAX_BUDGET_INCREASE_PERCENT', 50))
    MIN_PERFORMANCE_SCORE = float(os.getenv('MIN_PERFORMANCE_SCORE', 0.4))
    HIGH_PERFORMANCE_THRESHOLD = float(os.getenv('HIGH_PERFORMANCE_THRESHOLD', 0.8))
    
    # Celery Configuration
    CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0')
    CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')
    
    # File Upload Settings
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'uploads/')
    MAX_FILE_SIZE = int(os.getenv('MAX_FILE_SIZE', 10485760))  # 10MB
    ALLOWED_EXTENSIONS = set(os.getenv('ALLOWED_EXTENSIONS', 'csv,json,xlsx').split(','))
    
    # Feature Flags
    FEATURE_AI_OPTIMIZATION = os.getenv('FEATURE_AI_OPTIMIZATION', 'True').lower() == 'true'
    FEATURE_AUTO_PAUSE = os.getenv('FEATURE_AUTO_PAUSE', 'True').lower() == 'true'
    FEATURE_PREDICTIVE_ANALYTICS = os.getenv('FEATURE_PREDICTIVE_ANALYTICS', 'True').lower() == 'true'
    
    @staticmethod
    def init_app(app):
        """Initialize application configuration"""
        pass


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False


class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
