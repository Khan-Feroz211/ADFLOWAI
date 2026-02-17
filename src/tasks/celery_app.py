"""
ADFLOWAI - Celery Tasks
Background task processing for campaign optimization
"""

import os
import logging
from celery import Celery
from celery.schedules import crontab

logger = logging.getLogger(__name__)

# ── Create Celery App ────────────────────────────────────────────────────────

def make_celery():
    broker = os.getenv('CELERY_BROKER_URL', 'redis://redis:6379/0')
    backend = os.getenv('CELERY_RESULT_BACKEND', 'redis://redis:6379/0')
    
    app = Celery(
        'adflowai',
        broker=broker,
        backend=backend,
        include=['src.tasks.celery_app']
    )
    
    app.conf.update(
        task_serializer='json',
        accept_content=['json'],
        result_serializer='json',
        timezone='UTC',
        enable_utc=True,
        task_track_started=True,
        task_acks_late=True,
        worker_prefetch_multiplier=1,
        # Scheduled tasks
        beat_schedule={
            'optimize-all-campaigns-hourly': {
                'task': 'src.tasks.celery_app.optimize_all_campaigns',
                'schedule': crontab(minute=0),  # Every hour
            },
            'sync-metrics-daily': {
                'task': 'src.tasks.celery_app.sync_all_metrics',
                'schedule': crontab(hour=2, minute=0),  # Daily at 2 AM UTC
            },
        }
    )
    
    return app


celery_app = make_celery()


# ── Tasks ────────────────────────────────────────────────────────────────────

@celery_app.task(bind=True, max_retries=3, default_retry_delay=60)
def optimize_campaign_task(self, campaign_id: int):
    """
    Background task: Run AI optimization on a single campaign
    
    Args:
        campaign_id: ID of the campaign to optimize
    """
    try:
        logger.info(f"[TASK] Optimizing campaign {campaign_id}")
        
        # Import here to avoid circular imports
        from app import create_app
        from src.core.campaign_manager import CampaignManager
        
        flask_app = create_app()
        with flask_app.app_context():
            manager = CampaignManager()
            actions = manager.optimize_campaign(campaign_id)
            logger.info(f"[TASK] Campaign {campaign_id} optimized: {actions}")
            return {'campaign_id': campaign_id, 'actions': actions, 'status': 'success'}
        
    except Exception as exc:
        logger.error(f"[TASK] Error optimizing campaign {campaign_id}: {exc}")
        raise self.retry(exc=exc)


@celery_app.task(bind=True, max_retries=3)
def optimize_all_campaigns(self):
    """
    Background task: Optimize all active campaigns (runs hourly)
    """
    try:
        logger.info("[TASK] Running scheduled optimization for all campaigns")
        
        from app import create_app
        from src.core.campaign_manager import CampaignManager
        from src.models.campaign import Campaign, CampaignStatus
        
        flask_app = create_app()
        with flask_app.app_context():
            from src.core.database import db
            session = db.get_session()
            
            # Get all active campaigns
            active = session.query(Campaign).filter_by(
                status=CampaignStatus.ACTIVE
            ).all()
            
            results = []
            for campaign in active:
                try:
                    manager = CampaignManager()
                    actions = manager.optimize_campaign(campaign.id)
                    results.append({'campaign_id': campaign.id, 'actions': actions})
                except Exception as e:
                    logger.error(f"[TASK] Failed to optimize campaign {campaign.id}: {e}")
                    results.append({'campaign_id': campaign.id, 'error': str(e)})
            
            session.close()
            logger.info(f"[TASK] Scheduled optimization complete. {len(results)} campaigns processed.")
            return results
        
    except Exception as exc:
        logger.error(f"[TASK] Scheduled optimization failed: {exc}")
        raise self.retry(exc=exc)


@celery_app.task(bind=True, max_retries=3)
def sync_all_metrics(self):
    """
    Background task: Sync metrics from all platform APIs (runs daily)
    In production this would call Google/Facebook/etc. APIs
    """
    try:
        logger.info("[TASK] Syncing metrics from all platforms")
        # TODO: Implement real platform API calls here
        # For now just log
        logger.info("[TASK] Metrics sync complete (stub - add real API calls)")
        return {'status': 'success', 'message': 'Metrics synced'}
    
    except Exception as exc:
        logger.error(f"[TASK] Metrics sync failed: {exc}")
        raise self.retry(exc=exc)
