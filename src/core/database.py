"""
ADFLOWAI - Database Layer
SQLAlchemy setup with proper pool handling for both Postgres and SQLite
"""

import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.pool import QueuePool, StaticPool

from src.models.campaign import Base

logger = logging.getLogger(__name__)


class Database:
    def __init__(self):
        self.engine = None
        self.Session = None

    def init_app(self, app):
        url = app.config["SQLALCHEMY_DATABASE_URI"]

        # SQLite (testing) needs special pool settings
        if url.startswith("sqlite"):
            self.engine = create_engine(
                url,
                connect_args={"check_same_thread": False},
                poolclass=StaticPool,
            )
        else:
            self.engine = create_engine(
                url,
                poolclass=QueuePool,
                pool_size=app.config.get("SQLALCHEMY_POOL_SIZE", 10),
                max_overflow=app.config.get("SQLALCHEMY_MAX_OVERFLOW", 5),
                pool_timeout=app.config.get("SQLALCHEMY_POOL_TIMEOUT", 30),
                pool_pre_ping=True,
            )

        self.Session = scoped_session(sessionmaker(bind=self.engine))
        app.db = self
        self.create_tables()
        logger.info(f"Database ready: {url.split('@')[-1] if '@' in url else url}")

    def create_tables(self):
        Base.metadata.create_all(self.engine)
        logger.info("Tables created / verified")

    def drop_tables(self):
        Base.metadata.drop_all(self.engine)
        logger.warning("All tables dropped")

    def get_session(self):
        return self.Session()

    def close_session(self):
        self.Session.remove()


# Singleton
db = Database()


def init_db(app):
    db.init_app(app)

    @app.teardown_appcontext
    def shutdown_session(exc=None):
        db.close_session()


def get_db_session():
    """
    Returns an active SQLAlchemy session.
    Must be called from within a Flask app context (i.e. inside a route or with app.app_context()).
    """
    if db.Session is None:
        raise RuntimeError(
            "Database not initialised. Call init_db(app) before using get_db_session()."
        )
    return db.get_session()
