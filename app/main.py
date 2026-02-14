from fastapi import FastAPI
from app.api.v1 import adaptation, analysis, videos
from app.core.logging import configure_logging

configure_logging()

app = FastAPI(title="video_ai_agent", version="2.0.0")
app.include_router(videos.router, prefix="/api/v1")
app.include_router(analysis.router, prefix="/api/v1")
app.include_router(adaptation.router, prefix="/api/v1")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
