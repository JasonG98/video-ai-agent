from app.agent.schemas import GenerationOutput, PerceptionOutput, ReasoningOutput, UnderstandingOutput
from app.schemas.adaptation import ProductInfo


class GenerationLayer:
    def run(
        self,
        perception: PerceptionOutput,
        understanding: UnderstandingOutput,
        reasoning: ReasoningOutput,
        product_info: ProductInfo,
    ) -> GenerationOutput:
        """生成逐镜头改编脚本与执行文档。"""
        adapted_script = []
        for shot in perception.shots:
            adapted_script.append(
                {
                    "index": shot.index,
                    "original_summary": shot.transcript or shot.scene,
                    "adapted_script": f"[{product_info.brand_tone}] {product_info.name} {product_info.selling_points[0] if product_info.selling_points else '高价值'}",
                    "visual_direction": f"保留{shot.scene}场景，突出{product_info.category}质感",
                    "cta": "立即点击了解" if shot.index == len(perception.shots) - 1 else None,
                }
            )
        execution_docs = {
            "shooting_notes": ["保持前3秒出现产品", "口播节奏与原视频一致"],
            "editing_notes": ["字幕使用高对比色", "每镜头转场<0.3s"],
            "risk_checks": reasoning.recommendations,
        }
        return GenerationOutput(
            adapted_script=adapted_script,
            execution_docs=execution_docs,
            metadata={"narrative_structure": understanding.narrative_structure},
        )
