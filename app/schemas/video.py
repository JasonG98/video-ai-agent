from datetime import datetime
from pydantic import BaseModel


class VideoUploadResponse(BaseModel):
    video_id: int
    status: str
    storage_url: str


class VideoResponse(BaseModel):
    id: int
    filename: str
    content_type: str
    size_bytes: int
    duration_sec: float | None
    storage_key: str
    created_at: datetime

    class Config:
        from_attributes = True
