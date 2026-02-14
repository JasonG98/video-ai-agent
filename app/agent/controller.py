from datetime import datetime
from app.agent.generation import GenerationLayer
from app.agent.perception import PerceptionLayer
from app.agent.reasoning import ReasoningLayer
from app.agent.schemas import AgentState
from app.agent.understanding import UnderstandingLayer
from app.schemas.adaptation import ProductInfo


class VideoAnalysisAgent:
    def __init__(self) -> None:
        self.perception = PerceptionLayer()
        self.understanding = UnderstandingLayer()
        self.reasoning = ReasoningLayer()
        self.generation = GenerationLayer()

    def _trace(self, state: AgentState, phase: str, message: str, progress: int) -> None:
        state.progress = progress
        state.last_message = message
        state.reasoning_trace.append({"timestamp": datetime.utcnow(), "phase": phase, "message": message})

    def analyze_and_adapt(self, video_path: str, new_product_info: ProductInfo | None = None) -> dict:
        """运行完整四层分析，并可选做改编。"""
        state = AgentState()
        self._trace(state, "perception", "开始镜头/语音/图像感知", 20)
        perception = self.perception.run(video_path)
        self._trace(state, "understanding", "开始叙事理解", 45)
        understanding = self.understanding.run(perception)
        self._trace(state, "reasoning", "开始规则推理", 70)
        reasoning = self.reasoning.run(perception, understanding)

        result = {
            "perception": perception.model_dump(),
            "understanding": understanding.model_dump(),
            "reasoning": reasoning.model_dump(),
            "trace": [item if isinstance(item, dict) else item.model_dump() for item in state.reasoning_trace],
        }

        if new_product_info:
            self._trace(state, "generation", "开始生成改编脚本", 90)
            generation = self.generation.run(perception, understanding, reasoning, new_product_info)
            result["generation"] = generation.model_dump()

        self._trace(state, "done", "处理完成", 100)
        result["trace"] = [item if isinstance(item, dict) else item.model_dump() for item in state.reasoning_trace]
        return result
