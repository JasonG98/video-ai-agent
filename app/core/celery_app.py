from celery import Celery
from app.config import get_settings

settings = get_settings()

celery_app = Celery(
    "video_ai_agent",
    broker=settings.effective_celery_broker,
    backend=settings.effective_celery_backend,
    include=["app.tasks.analysis_tasks", "app.tasks.adaptation_tasks"],
)

celery_app.conf.update(
    task_track_started=True,
    timezone="UTC",
    result_expires=3600,
)
