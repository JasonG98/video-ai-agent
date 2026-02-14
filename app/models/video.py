from datetime import datetime
from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.db import Base


class Video(Base):
    __tablename__ = "videos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    filename: Mapped[str] = mapped_column(String(255), nullable=False)
    content_type: Mapped[str] = mapped_column(String(128), nullable=False)
    size_bytes: Mapped[int] = mapped_column(Integer, nullable=False)
    duration_sec: Mapped[float | None] = mapped_column(nullable=True)
    storage_key: Mapped[str] = mapped_column(String(512), unique=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)

    shots = relationship("Shot", back_populates="video", cascade="all, delete-orphan")
    analyses = relationship("Analysis", back_populates="video", cascade="all, delete-orphan")
