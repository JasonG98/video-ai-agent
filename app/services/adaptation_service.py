import traceback
from sqlalchemy.orm import Session
from app.agent.controller import VideoAnalysisAgent
from app.models.adaptation import Adaptation
from app.models.analysis import Analysis
from app.models.video import Video
from app.schemas.adaptation import ProductInfo


class AdaptationService:
    def __init__(self, db: Session):
        self.db = db
        self.agent = VideoAnalysisAgent()

    def create_adaptation(self, analysis_id: int, product_info: ProductInfo) -> Adaptation:
        adaptation = Adaptation(
            analysis_id=analysis_id,
            status="queued",
            progress=0,
            last_message="任务已入队",
            product_info_json=product_info.model_dump(),
        )
        self.db.add(adaptation)
        self.db.commit()
        self.db.refresh(adaptation)
        return adaptation

    def get_adaptation(self, adaptation_id: int) -> Adaptation | None:
        return self.db.get(Adaptation, adaptation_id)

    def run_adaptation(self, adaptation_id: int) -> None:
        adaptation = self.db.get(Adaptation, adaptation_id)
        if not adaptation:
            raise ValueError("adaptation not found")
        analysis = self.db.get(Analysis, adaptation.analysis_id)
        if not analysis:
            raise ValueError("analysis not found")
        video = self.db.get(Video, analysis.video_id)
        if not video:
            raise ValueError("video not found")
        try:
            adaptation.status = "processing"
            adaptation.progress = 20
            adaptation.last_message = "改编中"
            self.db.commit()

            product_info = ProductInfo(**adaptation.product_info_json)
            result = self.agent.analyze_and_adapt(video.storage_key, new_product_info=product_info)
            adaptation.result_json = result.get("generation", {})
            adaptation.trace_json = result.get("trace", [])
            adaptation.status = "succeeded"
            adaptation.progress = 100
            adaptation.last_message = "改编完成"
            self.db.commit()
        except Exception:
            adaptation.status = "failed"
            adaptation.progress = 100
            adaptation.last_message = "改编失败"
            adaptation.error = traceback.format_exc()
            self.db.commit()
