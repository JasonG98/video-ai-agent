from app.agent.schemas import GenerationOutput, PerceptionOutput, ReasoningOutput, UnderstandingOutput
from app.ai_models.llm_client import LLMClient
from app.schemas.adaptation import ProductInfo
from app.utils.prompt_builder import (
    build_copywriting_prompt,
    build_pattern_prompt,
    build_shot_adaptation_prompt,
)


class GenerationLayer:
    def __init__(self) -> None:
        self.llm = LLMClient()

    def run(
        self,
        perception: PerceptionOutput,
        understanding: UnderstandingOutput,
        reasoning: ReasoningOutput,
        product_info: ProductInfo,
    ) -> GenerationOutput:
        """生成逐镜头改编脚本与执行文档（接入 LLM 结构化输出）。"""
        style_prompt = build_copywriting_prompt(product_info.name, product_info.brand_tone)
        pattern_prompt = build_pattern_prompt(reasoning.recommendations)
        base_schema = {
            "type": "object",
            "properties": {
                "script": {"type": "string"},
                "visual_direction": {"type": "string"},
                "cta": {"type": "string"},
            },
            "required": ["script", "visual_direction", "cta"],
        }

        adapted_script = []
        for shot in perception.shots:
            shot_prompt = (
                f"{style_prompt}\n{pattern_prompt}\n"
                f"{build_shot_adaptation_prompt(shot.transcript or shot.scene, product_info.model_dump())}"
            )
            shot_output = self.llm.complete_structured(shot_prompt, base_schema)
            adapted_script.append(
                {
                    "index": shot.index,
                    "original_summary": shot.transcript or shot.scene,
                    "adapted_script": shot_output.get("script")
                    or f"[{product_info.brand_tone}] {product_info.name} {product_info.selling_points[0] if product_info.selling_points else '高价值'}",
                    "visual_direction": shot_output.get("visual_direction")
                    or f"保留{shot.scene}场景，突出{product_info.category}质感",
                    "cta": shot_output.get("cta") if shot.index == len(perception.shots) - 1 else None,
                }
            )

        execution_docs = {
            "shooting_notes": ["保持前3秒出现产品", "口播节奏与原视频一致"],
            "editing_notes": ["字幕使用高对比色", "每镜头转场<0.3s"],
            "risk_checks": reasoning.recommendations,
            "llm_notes": {
                "narrative_focus": understanding.key_hooks[:2],
                "product": product_info.model_dump(),
            },
        }
        return GenerationOutput(
            adapted_script=adapted_script,
            execution_docs=execution_docs,
            metadata={"narrative_structure": understanding.narrative_structure},
        )
