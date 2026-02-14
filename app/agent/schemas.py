from datetime import datetime
from pydantic import BaseModel, Field


class ShotSchema(BaseModel):
    index: int
    start_time: float
    end_time: float
    duration: float
    transcript: str = ""
    objects: list[str] = Field(default_factory=list)
    scene: str = "unknown"


class PerceptionOutput(BaseModel):
    shots: list[ShotSchema]
    transcript_summary: str


class UnderstandingOutput(BaseModel):
    narrative_structure: dict
    emotional_curve: list[dict]
    key_hooks: list[str]


class ReasoningOutput(BaseModel):
    rules_result: dict
    recommendations: list[str]


class AdaptedShot(BaseModel):
    index: int
    original_summary: str
    adapted_script: str
    visual_direction: str
    cta: str | None = None


class GenerationOutput(BaseModel):
    adapted_script: list[AdaptedShot]
    execution_docs: dict
    metadata: dict


class ReasoningTrace(BaseModel):
    timestamp: datetime
    phase: str
    message: str


class AgentState(BaseModel):
    progress: int = 0
    last_message: str = ""
    reasoning_trace: list[ReasoningTrace] = Field(default_factory=list)
