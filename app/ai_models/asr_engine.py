class ASREngine:
    """TODO: 可替换为 Whisper。"""

    def transcribe(self, video_path: str) -> dict[int, str]:
        return {
            0: "开场展示产品核心亮点",
            1: "演示使用场景与对比效果",
            2: "强调真实反馈与保障",
            3: "立即下单领取优惠",
        }
