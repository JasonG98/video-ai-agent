from pydantic import BaseModel


class DetectedShot(BaseModel):
    index: int
    start_time: float
    end_time: float
    duration: float


class SceneDetector:
    """TODO: 可替换为 PySceneDetect。"""

    def detect_shots(self, video_path: str) -> list[DetectedShot]:
        # MVP 使用固定均匀切片。
        total_duration = 12.0
        segments = 4
        step = total_duration / segments
        return [
            DetectedShot(index=i, start_time=round(i * step, 2), end_time=round((i + 1) * step, 2), duration=round(step, 2))
            for i in range(segments)
        ]
