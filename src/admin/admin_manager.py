"""
ADFLOWAI - Admin Manager
User management and system statistics
"""
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from sqlalchemy import func

from src.models.campaign import User, Campaign, CampaignStatus, OptimizationLog
from src.core.database import get_db_session

logger = logging.getLogger(__name__)


class AdminManager:
    def __init__(self, db_session=None):
        self._db = db_session

    @property
    def db(self):
        if self._db is None:
            self._db = get_db_session()
        return self._db

    # ── Users ──────────────────────────────────────────────────────────────

    def get_all_users(self, page=1, per_page=20, search=None) -> Dict:
        q = self.db.query(User)
        if search:
            q = q.filter(
                User.username.ilike(f'%{search}%') |
                User.email.ilike(f'%{search}%') |
                User.company.ilike(f'%{search}%')
            )
        total = q.count()
        users = q.order_by(User.created_at.desc()).offset((page-1)*per_page).limit(per_page).all()
        return {
            'users': [self._user_dict(u) for u in users],
            'total': total, 'page': page,
            'per_page': per_page,
            'pages': max(1, (total + per_page - 1) // per_page)
        }

    def get_user(self, user_id: int) -> Optional[User]:
        return self.db.query(User).filter_by(id=user_id).first()

    def update_user(self, user_id: int, data: Dict) -> User:
        user = self.get_user(user_id)
        if not user:
            raise ValueError(f"User {user_id} not found")
        for k in ('full_name', 'company', 'role', 'is_active', 'is_verified'):
            if k in data:
                setattr(user, k, data[k])
        self.db.commit()
        self.db.refresh(user)
        return user

    def delete_user(self, user_id: int) -> bool:
        user = self.get_user(user_id)
        if not user:
            raise ValueError(f"User {user_id} not found")
        self.db.delete(user)
        self.db.commit()
        return True

    def toggle_active(self, user_id: int) -> User:
        user = self.get_user(user_id)
        if not user:
            raise ValueError(f"User {user_id} not found")
        user.is_active = not user.is_active
        self.db.commit()
        self.db.refresh(user)
        return user

    def set_role(self, user_id: int, role: str) -> User:
        if role not in ('user', 'admin', 'agency'):
            raise ValueError(f"Invalid role: {role}")
        return self.update_user(user_id, {'role': role})

    # ── System Stats ────────────────────────────────────────────────────────

    def get_system_stats(self) -> Dict:
        week_ago = datetime.utcnow() - timedelta(days=7)

        total_users     = self.db.query(func.count(User.id)).scalar() or 0
        active_users    = self.db.query(func.count(User.id)).filter_by(is_active=True).scalar() or 0
        new_users_week  = self.db.query(func.count(User.id)).filter(User.created_at >= week_ago).scalar() or 0

        total_campaigns   = self.db.query(func.count(Campaign.id)).scalar() or 0
        active_campaigns  = self.db.query(func.count(Campaign.id)).filter_by(status=CampaignStatus.ACTIVE).scalar() or 0
        new_camps_week    = self.db.query(func.count(Campaign.id)).filter(Campaign.created_at >= week_ago).scalar() or 0

        total_budget = self.db.query(func.sum(Campaign.total_budget)).scalar() or 0
        total_spent  = self.db.query(func.sum(Campaign.spent_budget)).scalar() or 0
        total_opts   = self.db.query(func.count(OptimizationLog.id)).scalar() or 0

        return {
            'users':     {'total': total_users, 'active': active_users, 'new_this_week': new_users_week},
            'campaigns': {'total': total_campaigns, 'active': active_campaigns, 'new_this_week': new_camps_week},
            'financials': {
                'total_budget_managed': round(float(total_budget), 2),
                'total_spent':          round(float(total_spent), 2),
                'avg_budget':           round(float(total_budget)/total_campaigns, 2) if total_campaigns else 0,
            },
            'ai': {'total_optimizations': total_opts},
        }

    def get_recent_activity(self, limit=20) -> List[Dict]:
        logs = self.db.query(OptimizationLog)\
                   .order_by(OptimizationLog.performed_at.desc())\
                   .limit(limit).all()
        return [{
            'id': l.id,
            'campaign_id': l.campaign_id,
            'action': l.action,
            'reason': l.reason,
            'success': l.success,
            'confidence_score': l.confidence_score,
            'performed_at': l.performed_at.isoformat() if l.performed_at else None,
        } for l in logs]

    # ── Helper ──────────────────────────────────────────────────────────────

    def _user_dict(self, u: User) -> Dict:
        camp_count = self.db.query(func.count(Campaign.id)).filter_by(user_id=u.id).scalar() or 0
        return {
            'id': u.id, 'username': u.username, 'email': u.email,
            'full_name': u.full_name, 'company': u.company,
            'role': u.role, 'is_active': u.is_active, 'is_verified': u.is_verified,
            'campaign_count': camp_count,
            'created_at': u.created_at.isoformat() if u.created_at else None,
            'last_login':  u.last_login.isoformat()  if u.last_login  else None,
        }
