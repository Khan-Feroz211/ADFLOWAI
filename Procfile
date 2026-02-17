web: gunicorn --bind 0.0.0.0:$PORT --workers 2 --threads 2 --timeout 60 app:app
worker: celery -A src.tasks.celery_app worker --loglevel=info --concurrency=2
