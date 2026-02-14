from sqlalchemy import ForeignKey, Integer
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.db import Base


class Shot(Base):
    __tablename__ = "shots"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    video_id: Mapped[int] = mapped_column(ForeignKey("videos.id", ondelete="CASCADE"), index=True)
    index: Mapped[int] = mapped_column(Integer, nullable=False)
    start_time: Mapped[float] = mapped_column(nullable=False)
    end_time: Mapped[float] = mapped_column(nullable=False)
    keyframe_path: Mapped[str | None] = mapped_column(nullable=True)
    analysis_json: Mapped[dict] = mapped_column(JSONB, default=dict)

    video = relationship("Video", back_populates="shots")
