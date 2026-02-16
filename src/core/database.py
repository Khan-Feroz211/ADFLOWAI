"""
ADFLOWAI Database Initialization
Setup and management of database connections
"""

import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.pool import QueuePool

from src.models.campaign import Base

logger = logging.getLogger(__name__)


class Database:
    """Database manager class"""
    
    def __init__(self, app=None):
        self.engine = None
        self.session_factory = None
        self.Session = None
        
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        """
        Initialize database with Flask app
        
        Args:
            app: Flask application instance
        """
        database_url = app.config['SQLALCHEMY_DATABASE_URI']
        
        # Create engine with connection pooling
        self.engine = create_engine(
            database_url,
            poolclass=QueuePool,
            pool_size=app.config.get('SQLALCHEMY_POOL_SIZE', 20),
            max_overflow=app.config.get('SQLALCHEMY_MAX_OVERFLOW', 10),
            pool_timeout=app.config.get('SQLALCHEMY_POOL_TIMEOUT', 30),
            pool_pre_ping=True,  # Verify connections before using
            echo=app.config.get('SQL_ECHO', False)
        )
        
        # Create session factory
        self.session_factory = sessionmaker(bind=self.engine)
        self.Session = scoped_session(self.session_factory)
        
        logger.info(f"Database initialized: {database_url.split('@')[-1]}")
        
        # Store in app context
        app.db = self
        
        # Create tables if they don't exist
        self.create_tables()
    
    def create_tables(self):
        """Create all database tables"""
        try:
            Base.metadata.create_all(self.engine)
            logger.info("Database tables created successfully")
        except Exception as e:
            logger.error(f"Error creating database tables: {str(e)}")
            raise
    
    def drop_tables(self):
        """Drop all database tables (use with caution!)"""
        try:
            Base.metadata.drop_all(self.engine)
            logger.warning("All database tables dropped")
        except Exception as e:
            logger.error(f"Error dropping database tables: {str(e)}")
            raise
    
    def get_session(self):
        """
        Get a new database session
        
        Returns:
            SQLAlchemy session object
        """
        return self.Session()
    
    def close_session(self):
        """Close the current session"""
        self.Session.remove()


# Global database instance
db = Database()


def init_db(app):
    """
    Initialize database with application
    
    Args:
        app: Flask application instance
    """
    db.init_app(app)
    
    # Register teardown handler
    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db.close_session()


def get_db_session():
    """
    Get database session for dependency injection
    
    Returns:
        SQLAlchemy session
    """
    return db.get_session()
