"""
ADFLOWAI - Authentication Manager
Fixed version: db session passed in per-call, not at init
"""

import bcrypt
import logging
from datetime import datetime, timedelta
from typing import Optional, Dict, Tuple
from flask_jwt_extended import create_access_token, create_refresh_token

from src.models.campaign import User

logger = logging.getLogger(__name__)


class AuthenticationError(Exception):
    """Raised when authentication fails"""
    pass


class AuthManager:
    """
    Manages user authentication.
    Always pass a db_session from the caller - never resolves it at import time.
    """

    def __init__(self, db_session):
        """
        Args:
            db_session: Active SQLAlchemy session (from get_db_session() inside a route)
        """
        self.db = db_session
        self.password_min_length = 8

    # ── Public methods ──────────────────────────────────────────────────────

    def register_user(
        self,
        username: str,
        email: str,
        password: str,
        full_name: Optional[str] = None,
        company: Optional[str] = None,
    ) -> Tuple[User, Dict]:
        """Register a new user and return (user, tokens)."""
        self._validate_registration(username, email, password)

        existing = self.db.query(User).filter(
            (User.username == username) | (User.email == email)
        ).first()

        if existing:
            if existing.username == username:
                raise AuthenticationError("Username already exists")
            raise AuthenticationError("Email already exists")

        user = User(
            username=username,
            email=email,
            password_hash=self._hash_password(password),
            full_name=full_name,
            company=company,
            is_active=True,
            is_verified=False,
            role="user",
        )

        try:
            self.db.add(user)
            self.db.commit()
            self.db.refresh(user)
        except Exception as e:
            self.db.rollback()
            logger.error(f"DB error on register: {e}")
            raise AuthenticationError("Registration failed - database error")

        tokens = self._generate_tokens(user)
        logger.info(f"User registered: {username}")
        return user, tokens

    def login(self, username_or_email: str, password: str) -> Tuple[User, Dict]:
        """Authenticate user, return (user, tokens)."""
        user = self.db.query(User).filter(
            (User.username == username_or_email) | (User.email == username_or_email)
        ).first()

        if not user:
            raise AuthenticationError("Invalid username or password")
        if not user.is_active:
            raise AuthenticationError("Account is disabled")
        if not self._verify_password(password, user.password_hash):
            raise AuthenticationError("Invalid username or password")

        try:
            user.last_login = datetime.utcnow()
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            logger.warning(f"Could not update last_login: {e}")

        tokens = self._generate_tokens(user)
        logger.info(f"User logged in: {user.username}")
        return user, tokens

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        return self.db.query(User).filter_by(id=user_id).first()

    def refresh_access_token(self, user_id: int) -> str:
        user = self.get_user_by_id(user_id)
        if not user or not user.is_active:
            raise AuthenticationError("User not found or inactive")
        return create_access_token(
            identity=user_id,
            additional_claims={"username": user.username, "role": user.role},
        )

    def change_password(self, user_id: int, old_password: str, new_password: str) -> bool:
        user = self.get_user_by_id(user_id)
        if not user:
            raise AuthenticationError("User not found")
        if not self._verify_password(old_password, user.password_hash):
            raise AuthenticationError("Current password is incorrect")
        if len(new_password) < self.password_min_length:
            raise AuthenticationError(
                f"New password must be at least {self.password_min_length} characters"
            )
        user.password_hash = self._hash_password(new_password)
        self.db.commit()
        logger.info(f"Password changed for user {user_id}")
        return True

    # ── Private helpers ─────────────────────────────────────────────────────

    def _validate_registration(self, username: str, email: str, password: str):
        if not username or len(username) < 3:
            raise AuthenticationError("Username must be at least 3 characters")
        if len(username) > 50:
            raise AuthenticationError("Username must be under 50 characters")
        if not username.replace("_", "").replace("-", "").isalnum():
            raise AuthenticationError("Username may only contain letters, digits, _ or -")
        if not email or "@" not in email:
            raise AuthenticationError("Invalid email address")
        if len(password) < self.password_min_length:
            raise AuthenticationError(
                f"Password must be at least {self.password_min_length} characters"
            )
        if not (
            any(c.isupper() for c in password)
            and any(c.islower() for c in password)
            and any(c.isdigit() for c in password)
        ):
            raise AuthenticationError(
                "Password must contain uppercase letters, lowercase letters, and numbers"
            )

    def _hash_password(self, password: str) -> str:
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    def _verify_password(self, password: str, hashed: str) -> bool:
        return bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))

    def _generate_tokens(self, user: User) -> Dict:
        access = create_access_token(
            identity=user.id,
            additional_claims={
                "username": user.username,
                "email": user.email,
                "role": user.role,
            },
            expires_delta=timedelta(hours=1),
        )
        refresh = create_refresh_token(
            identity=user.id,
            expires_delta=timedelta(days=30),
        )
        return {
            "access_token": access,
            "refresh_token": refresh,
            "token_type": "Bearer",
            "expires_in": 3600,
        }
