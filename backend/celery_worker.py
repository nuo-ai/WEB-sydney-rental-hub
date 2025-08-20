from celery_config import celery_app

# This is the entry point for the Celery worker.
# To run the worker, use the following command from the project root:
# celery -A backend.celery_worker.celery_app worker --loglevel=info
