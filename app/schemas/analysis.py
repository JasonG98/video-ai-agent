from pydantic import BaseModel
from app.schemas.common import TaskStatus


class AnalysisRunResponse(BaseModel):
    analysis_id: int
    status: TaskStatus


class AnalysisResultResponse(BaseModel):
    analysis_id: int
    perception: dict
    understanding: dict
    reasoning: dict
    trace: list[dict] = []
