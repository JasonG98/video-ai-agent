from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.schemas.video import VideoResponse, VideoUploadResponse
from app.services.video_service import VideoService

router = APIRouter(prefix="/videos", tags=["videos"])


@router.post("/upload", response_model=VideoUploadResponse)
async def upload_video(file: UploadFile = File(...), db: Session = Depends(get_db)) -> VideoUploadResponse:
    content = await file.read()
    if not content:
        raise HTTPException(status_code=400, detail="empty file")
    video = VideoService(db).upload_video(file.filename, file.content_type or "video/mp4", content)
    return VideoUploadResponse(video_id=video.id, status="uploaded", storage_url=getattr(video, "storage_url", video.storage_key))


@router.get("/{video_id}", response_model=VideoResponse)
def get_video(video_id: int, db: Session = Depends(get_db)) -> VideoResponse:
    video = VideoService(db).get_video(video_id)
    if not video:
        raise HTTPException(status_code=404, detail="video not found")
    return VideoResponse.model_validate(video)
