class ImageAnalyzer:
    """TODO: 可替换为 CLIP/YOLO。"""

    def analyze_frame(self, video_path: str, shot_index: int) -> dict:
        mocks = [
            {"objects": ["product", "logo"], "scene": "closeup"},
            {"objects": ["user", "product"], "scene": "lifestyle"},
            {"objects": ["text", "badge"], "scene": "comparison"},
            {"objects": ["cta", "brand"], "scene": "ending"},
        ]
        return mocks[shot_index % len(mocks)]
