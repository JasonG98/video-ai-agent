from app.agent.schemas import PerceptionOutput, UnderstandingOutput
from app.ai_models.llm_client import LLMClient
from app.utils.prompt_builder import build_structure_prompt


class UnderstandingLayer:
    def __init__(self) -> None:
        self.llm = LLMClient()

    def run(self, perception: PerceptionOutput) -> UnderstandingOutput:
        """基于感知结果做叙事理解，并通过 LLM 生成结构化标签。"""
        hooks = [shot.transcript for shot in perception.shots if shot.index < 2 and shot.transcript]
        curve = [
            {"shot": shot.index, "emotion": "exciting" if shot.duration < 3 else "stable"}
            for shot in perception.shots
        ]
        structure = {
            "opening": [s.index for s in perception.shots[:2]],
            "body": [s.index for s in perception.shots[2:-1]],
            "ending": [s.index for s in perception.shots[-1:]],
        }

        prompt = build_structure_prompt(perception.transcript_summary or "无摘要")
        schema = {
            "type": "object",
            "properties": {
                "key_hooks": {"type": "array", "items": {"type": "string"}},
                "structure_hint": {"type": "string"},
            },
            "required": ["key_hooks", "structure_hint"],
        }
        llm_output = self.llm.complete_structured(prompt, schema)
        llm_hooks = llm_output.get("key_hooks", [])

        return UnderstandingOutput(
            narrative_structure={**structure, "llm_structure_hint": llm_output.get("structure_hint", "")},
            emotional_curve=curve,
            key_hooks=hooks or llm_hooks or ["前3秒给出核心卖点"],
        )
