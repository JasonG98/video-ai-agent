from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.db import Base


class Analysis(Base):
    __tablename__ = "analyses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    video_id: Mapped[int] = mapped_column(ForeignKey("videos.id", ondelete="CASCADE"), index=True)
    status: Mapped[str] = mapped_column(String(32), default="queued", index=True)
    progress: Mapped[int] = mapped_column(Integer, default=0)
    last_message: Mapped[str | None] = mapped_column(String(255), nullable=True)
    perception_json: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    understanding_json: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    reasoning_json: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    trace_json: Mapped[list | None] = mapped_column(JSONB, nullable=True)
    error: Mapped[str | None] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)

    video = relationship("Video", back_populates="analyses")
    adaptations = relationship("Adaptation", back_populates="analysis", cascade="all, delete-orphan")
