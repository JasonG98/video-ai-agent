import traceback
from sqlalchemy.orm import Session
from app.agent.controller import VideoAnalysisAgent
from app.models.analysis import Analysis
from app.models.video import Video
from app.utils.cache import get_json, set_json


class AnalysisService:
    def __init__(self, db: Session):
        self.db = db
        self.agent = VideoAnalysisAgent()

    def create_analysis(self, video_id: int) -> Analysis:
        analysis = Analysis(video_id=video_id, status="queued", progress=0, last_message="任务已入队")
        self.db.add(analysis)
        self.db.commit()
        self.db.refresh(analysis)
        return analysis

    def get_analysis(self, analysis_id: int) -> Analysis | None:
        return self.db.get(Analysis, analysis_id)

    def run_analysis(self, analysis_id: int) -> None:
        analysis = self.db.get(Analysis, analysis_id)
        if not analysis:
            raise ValueError("analysis not found")
        video = self.db.get(Video, analysis.video_id)
        if not video:
            raise ValueError("video not found")

        cache_key = f"analysis:video:{video.storage_key}"
        cached = get_json(cache_key)
        if cached:
            analysis.status = "succeeded"
            analysis.progress = 100
            analysis.last_message = "命中缓存"
            analysis.perception_json = cached["perception"]
            analysis.understanding_json = cached["understanding"]
            analysis.reasoning_json = cached["reasoning"]
            analysis.trace_json = cached.get("trace", [])
            self.db.commit()
            return

        try:
            analysis.status = "processing"
            analysis.progress = 10
            analysis.last_message = "分析中"
            self.db.commit()

            result = self.agent.analyze_and_adapt(video.storage_key)
            analysis.perception_json = result["perception"]
            analysis.understanding_json = result["understanding"]
            analysis.reasoning_json = result["reasoning"]
            analysis.trace_json = result.get("trace", [])
            analysis.status = "succeeded"
            analysis.progress = 100
            analysis.last_message = "分析完成"
            self.db.commit()
            set_json(cache_key, result)
        except Exception:
            analysis.status = "failed"
            analysis.progress = 100
            analysis.last_message = "分析失败"
            analysis.error = traceback.format_exc()
            self.db.commit()
