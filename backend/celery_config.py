import os
from celery import Celery
from dotenv import load_dotenv

load_dotenv()

# It's better to have a single, definitive source for the Celery app instance.
# This file will be that source.
# We will import this `celery_app` instance in other parts of the application.

# Get Redis URL from environment variables, with a default fallback
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

celery_app = Celery(
    "tasks",
    broker=REDIS_URL,
    backend=REDIS_URL,
    include=["backend.tasks"]  # Point to the tasks module
)

# Optional: Update Celery configuration with more settings if needed
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Australia/Sydney",
    enable_utc=True,
)

# The following is a good practice for larger applications,
# but for this simple case, direct configuration is fine.
# celery_app.config_from_object("backend.celeryconfig_object")
