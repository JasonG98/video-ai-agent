from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.schemas.analysis import AnalysisResultResponse, AnalysisRunResponse
from app.schemas.common import TaskStatusResponse
from app.services.analysis_service import AnalysisService
from app.services.video_service import VideoService
from app.tasks.analysis_tasks import analyze_video

router = APIRouter(prefix="/analysis", tags=["analysis"])


@router.post("/{video_id}/run", response_model=AnalysisRunResponse)
def run_analysis(video_id: int, db: Session = Depends(get_db)) -> AnalysisRunResponse:
    if not VideoService(db).get_video(video_id):
        raise HTTPException(status_code=404, detail="video not found")
    analysis = AnalysisService(db).create_analysis(video_id)
    analyze_video.delay(analysis.id)
    return AnalysisRunResponse(analysis_id=analysis.id, status="queued")


@router.get("/{analysis_id}/status", response_model=TaskStatusResponse)
def get_analysis_status(analysis_id: int, db: Session = Depends(get_db)) -> TaskStatusResponse:
    analysis = AnalysisService(db).get_analysis(analysis_id)
    if not analysis:
        raise HTTPException(status_code=404, detail="analysis not found")
    return TaskStatusResponse(
        id=analysis.id,
        status=analysis.status,
        progress=analysis.progress,
        last_message=analysis.last_message,
        error=analysis.error,
        updated_at=analysis.updated_at,
    )


@router.get("/{analysis_id}/result", response_model=AnalysisResultResponse)
def get_analysis_result(analysis_id: int, db: Session = Depends(get_db)) -> AnalysisResultResponse:
    analysis = AnalysisService(db).get_analysis(analysis_id)
    if not analysis:
        raise HTTPException(status_code=404, detail="analysis not found")
    if analysis.status != "succeeded":
        raise HTTPException(status_code=400, detail="analysis not completed")
    return AnalysisResultResponse(
        analysis_id=analysis.id,
        perception=analysis.perception_json or {},
        understanding=analysis.understanding_json or {},
        reasoning=analysis.reasoning_json or {},
        trace=analysis.trace_json or [],
    )
