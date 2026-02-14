from app.core.celery_app import celery_app
from app.core.db import SessionLocal
from app.services.adaptation_service import AdaptationService


@celery_app.task(name="app.tasks.adaptation_tasks.generate_adaptation")
def generate_adaptation(adaptation_id: int) -> None:
    db = SessionLocal()
    try:
        AdaptationService(db).run_adaptation(adaptation_id)
    finally:
        db.close()
