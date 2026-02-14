from datetime import datetime
from enum import Enum
from pydantic import BaseModel


class TaskStatus(str, Enum):
    queued = "queued"
    processing = "processing"
    succeeded = "succeeded"
    failed = "failed"


class TaskStatusResponse(BaseModel):
    id: int
    status: TaskStatus
    progress: int
    last_message: str | None = None
    error: str | None = None
    updated_at: datetime | None = None
