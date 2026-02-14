from app.agent.schemas import PerceptionOutput, ShotSchema
from app.ai_models.asr_engine import ASREngine
from app.ai_models.image_analyzer import ImageAnalyzer
from app.ai_models.scene_detector import SceneDetector


class PerceptionLayer:
    def __init__(self) -> None:
        self.scene_detector = SceneDetector()
        self.asr_engine = ASREngine()
        self.image_analyzer = ImageAnalyzer()

    def run(self, video_path: str) -> PerceptionOutput:
        """完成镜头、语音、图像感知并聚合。"""
        shots = self.scene_detector.detect_shots(video_path)
        transcript = self.asr_engine.transcribe(video_path)
        enriched: list[ShotSchema] = []
        for shot in shots:
            vision = self.image_analyzer.analyze_frame(video_path, shot.index)
            enriched.append(
                ShotSchema(
                    index=shot.index,
                    start_time=shot.start_time,
                    end_time=shot.end_time,
                    duration=shot.duration,
                    transcript=transcript.get(shot.index, ""),
                    objects=vision.get("objects", []),
                    scene=vision.get("scene", "unknown"),
                )
            )
        return PerceptionOutput(shots=enriched, transcript_summary=" ".join(transcript.values())[:200])
