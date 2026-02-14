from pydantic import BaseModel, Field
from app.schemas.common import TaskStatus


class ProductInfo(BaseModel):
    category: str
    name: str
    selling_points: list[str] = Field(default_factory=list)
    brand_tone: str


class AdaptationRunResponse(BaseModel):
    adaptation_id: int
    status: TaskStatus


class AdaptationResponse(BaseModel):
    id: int
    analysis_id: int
    status: TaskStatus
    progress: int
    last_message: str | None = None
    result_json: dict | None = None
    error: str | None = None

    class Config:
        from_attributes = True
