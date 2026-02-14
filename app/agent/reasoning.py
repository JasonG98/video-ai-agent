from statistics import mean
from app.agent.knowledge_base import KnowledgeBase
from app.agent.schemas import PerceptionOutput, ReasoningOutput, UnderstandingOutput


class ReasoningLayer:
    def run(self, perception: PerceptionOutput, understanding: UnderstandingOutput) -> ReasoningOutput:
        """执行规则引擎并生成建议。"""
        durations = [shot.duration for shot in perception.shots] or [0]
        avg_duration = mean(durations)
        first_product_time = perception.shots[0].start_time if perception.shots else 0
        has_cta = any(KnowledgeBase.has_cta(shot.transcript) for shot in perception.shots)

        recommendations: list[str] = []
        if first_product_time > 2:
            recommendations.append("建议产品在前2秒内出现")
        if avg_duration > 4:
            recommendations.append("镜头平均时长偏长，建议剪到3秒以内")
        if not has_cta:
            recommendations.append("结尾补充明确CTA，例如“立即下单”")
        if len(understanding.key_hooks) == 0:
            recommendations.append("增加开场钩子文案")
        if not recommendations:
            recommendations.append("当前结构良好，可直接替换商品信息进行复刻")

        return ReasoningOutput(
            rules_result={
                "first_product_time": first_product_time,
                "avg_shot_duration": avg_duration,
                "has_cta": has_cta,
                "shot_count": len(perception.shots),
            },
            recommendations=recommendations,
        )
