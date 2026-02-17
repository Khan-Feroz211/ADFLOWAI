"""
ADFLOWAI Database Models
SQLAlchemy ORM models for campaign management
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, JSON, ForeignKey, Text, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import enum

Base = declarative_base()


class CampaignStatus(enum.Enum):
    """Campaign status enumeration"""
    DRAFT = "draft"
    ACTIVE = "active"
    PAUSED = "paused"
    STOPPED = "stopped"
    COMPLETED = "completed"


class Platform(enum.Enum):
    """Advertising platform enumeration"""
    GOOGLE_ADS = "google_ads"
    FACEBOOK = "facebook"
    INSTAGRAM = "instagram"
    LINKEDIN = "linkedin"
    TWITTER = "twitter"
    TIKTOK = "tiktok"


class Campaign(Base):
    """Main campaign model"""
    __tablename__ = 'campaigns'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text)
    
    # Budget and financial
    total_budget = Column(Float, nullable=False)
    spent_budget = Column(Float, default=0.0)
    remaining_budget = Column(Float)
    
    # Campaign settings
    objective = Column(String(100))  # conversions, traffic, awareness, etc.
    status = Column(Enum(CampaignStatus), default=CampaignStatus.DRAFT, index=True)
    
    # Targeting
    target_audience = Column(JSON)  # Demographics, interests, locations
    
    # Dates
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Performance metrics
    impressions = Column(Integer, default=0)
    clicks = Column(Integer, default=0)
    conversions = Column(Integer, default=0)
    ctr = Column(Float, default=0.0)  # Click-through rate
    cpc = Column(Float, default=0.0)  # Cost per click
    cpa = Column(Float, default=0.0)  # Cost per acquisition
    roas = Column(Float, default=0.0)  # Return on ad spend
    
    # AI optimization
    performance_score = Column(Float, default=0.5)  # 0-1 scale
    ai_recommendations = Column(JSON)
    last_optimization = Column(DateTime)
    
    # Relationships
    platform_campaigns = relationship("PlatformCampaign", back_populates="campaign", cascade="all, delete-orphan")
    metrics_history = relationship("MetricsHistory", back_populates="campaign", cascade="all, delete-orphan")
    
    # User relationship (for multi-tenant)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)
    user = relationship("User", back_populates="campaigns")
    
    def __repr__(self):
        return f"<Campaign(id={self.id}, name='{self.name}', status='{self.status.value}')>"
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'total_budget': self.total_budget,
            'spent_budget': self.spent_budget,
            'remaining_budget': self.remaining_budget,
            'objective': self.objective,
            'status': self.status.value,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'metrics': {
                'impressions': self.impressions,
                'clicks': self.clicks,
                'conversions': self.conversions,
                'ctr': self.ctr,
                'cpc': self.cpc,
                'cpa': self.cpa,
                'roas': self.roas
            },
            'performance_score': self.performance_score,
            'created_at': self.created_at.isoformat()
        }


class PlatformCampaign(Base):
    """Platform-specific campaign details"""
    __tablename__ = 'platform_campaigns'
    
    id = Column(Integer, primary_key=True)
    campaign_id = Column(Integer, ForeignKey('campaigns.id'), nullable=False, index=True)
    
    platform = Column(Enum(Platform), nullable=False, index=True)
    platform_campaign_id = Column(String(255))  # ID from the platform's API
    
    # Budget allocation per platform
    allocated_budget = Column(Float, nullable=False)
    spent_budget = Column(Float, default=0.0)
    
    # Platform-specific metrics
    platform_metrics = Column(JSON)
    
    # Status
    is_active = Column(Boolean, default=True, index=True)
    last_synced = Column(DateTime)
    
    # Performance
    performance_score = Column(Float, default=0.5)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    campaign = relationship("Campaign", back_populates="platform_campaigns")
    
    def __repr__(self):
        return f"<PlatformCampaign(id={self.id}, platform='{self.platform.value}', campaign_id={self.campaign_id})>"


class MetricsHistory(Base):
    """Historical metrics for tracking performance over time"""
    __tablename__ = 'metrics_history'
    
    id = Column(Integer, primary_key=True)
    campaign_id = Column(Integer, ForeignKey('campaigns.id'), nullable=False, index=True)
    platform = Column(Enum(Platform), index=True)
    
    # Snapshot timestamp
    recorded_at = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Metrics snapshot
    impressions = Column(Integer, default=0)
    clicks = Column(Integer, default=0)
    conversions = Column(Integer, default=0)
    spent = Column(Float, default=0.0)
    
    # Calculated metrics
    ctr = Column(Float)
    cpc = Column(Float)
    cpa = Column(Float)
    roas = Column(Float)
    
    # Performance score at that time
    performance_score = Column(Float)
    
    # Relationships
    campaign = relationship("Campaign", back_populates="metrics_history")
    
    def __repr__(self):
        return f"<MetricsHistory(campaign_id={self.campaign_id}, recorded_at='{self.recorded_at}')>"


class User(Base):
    """User model for authentication and multi-tenancy"""
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False, index=True)
    email = Column(String(120), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    
    # Profile
    full_name = Column(String(255))
    company = Column(String(255))
    role = Column(String(50), default='user')  # user, admin, agency
    
    # Account status
    is_active = Column(Boolean, default=True, index=True)
    is_verified = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime)
    
    # Relationships
    campaigns = relationship("Campaign", back_populates="user", cascade="all, delete-orphan")
    api_keys = relationship("APIKey", back_populates="user", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}')>"


class APIKey(Base):
    """API keys for programmatic access"""
    __tablename__ = 'api_keys'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)
    
    key = Column(String(255), unique=True, nullable=False, index=True)
    name = Column(String(100))
    
    is_active = Column(Boolean, default=True, index=True)
    last_used = Column(DateTime)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime)
    
    # Relationships
    user = relationship("User", back_populates="api_keys")
    
    def __repr__(self):
        return f"<APIKey(id={self.id}, name='{self.name}')>"


class OptimizationLog(Base):
    """Log of AI optimization actions"""
    __tablename__ = 'optimization_logs'
    
    id = Column(Integer, primary_key=True)
    campaign_id = Column(Integer, ForeignKey('campaigns.id'), nullable=False, index=True)
    
    action = Column(String(100), nullable=False)  # budget_increase, budget_decrease, pause, resume, etc.
    reason = Column(Text)
    
    # Before and after state
    before_state = Column(JSON)
    after_state = Column(JSON)
    
    # AI confidence
    confidence_score = Column(Float)
    
    # Result
    success = Column(Boolean, default=True)
    error_message = Column(Text)
    
    performed_at = Column(DateTime, default=datetime.utcnow, index=True)
    
    def __repr__(self):
        return f"<OptimizationLog(id={self.id}, campaign_id={self.campaign_id}, action='{self.action}')>"
