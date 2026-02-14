from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from app.api.v1 import adaptation, analysis, videos
from app.core.logging import configure_logging

configure_logging()

app = FastAPI(title="video_ai_agent", version="2.0.0")
app.include_router(videos.router, prefix="/api/v1")
app.include_router(analysis.router, prefix="/api/v1")
app.include_router(adaptation.router, prefix="/api/v1")
webui_dir = Path(__file__).resolve().parent / "webui"
app.mount("/webui", StaticFiles(directory=webui_dir), name="webui")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/", include_in_schema=False)
def webui_index() -> FileResponse:
    return FileResponse(webui_dir / "index.html")
