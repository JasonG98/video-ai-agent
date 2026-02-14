from app.core.celery_app import celery_app
from app.core.db import SessionLocal
from app.services.analysis_service import AnalysisService


@celery_app.task(name="app.tasks.analysis_tasks.analyze_video")
def analyze_video(analysis_id: int) -> None:
    db = SessionLocal()
    try:
        AnalysisService(db).run_analysis(analysis_id)
    finally:
        db.close()
