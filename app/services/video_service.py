from sqlalchemy.orm import Session
from app.models.video import Video
from app.services.storage_service import StorageService


class VideoService:
    def __init__(self, db: Session):
        self.db = db
        self.storage = StorageService()

    def upload_video(self, filename: str, content_type: str, content: bytes) -> Video:
        key, storage_url = self.storage.save_file(filename, content, content_type)
        video = Video(
            filename=filename,
            content_type=content_type,
            size_bytes=len(content),
            duration_sec=None,
            storage_key=key,
        )
        self.db.add(video)
        self.db.commit()
        self.db.refresh(video)
        video.storage_url = storage_url
        return video

    def get_video(self, video_id: int) -> Video | None:
        return self.db.get(Video, video_id)
