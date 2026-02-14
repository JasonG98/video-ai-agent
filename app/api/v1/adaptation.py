from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.schemas.adaptation import AdaptationResponse, AdaptationRunResponse, ProductInfo
from app.services.adaptation_service import AdaptationService
from app.services.analysis_service import AnalysisService
from app.tasks.adaptation_tasks import generate_adaptation

router = APIRouter(prefix="/adaptation", tags=["adaptation"])


@router.post("/{analysis_id}/generate", response_model=AdaptationRunResponse)
def run_adaptation(analysis_id: int, body: ProductInfo, db: Session = Depends(get_db)) -> AdaptationRunResponse:
    analysis = AnalysisService(db).get_analysis(analysis_id)
    if not analysis:
        raise HTTPException(status_code=404, detail="analysis not found")
    adaptation = AdaptationService(db).create_adaptation(analysis_id, body)
    generate_adaptation.delay(adaptation.id)
    return AdaptationRunResponse(adaptation_id=adaptation.id, status="queued")


@router.get("/{adaptation_id}", response_model=AdaptationResponse)
def get_adaptation(adaptation_id: int, db: Session = Depends(get_db)) -> AdaptationResponse:
    adaptation = AdaptationService(db).get_adaptation(adaptation_id)
    if not adaptation:
        raise HTTPException(status_code=404, detail="adaptation not found")
    return AdaptationResponse.model_validate(adaptation)
