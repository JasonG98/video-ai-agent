from app.agent.schemas import PerceptionOutput, UnderstandingOutput


class UnderstandingLayer:
    def run(self, perception: PerceptionOutput) -> UnderstandingOutput:
        """基于感知结果做叙事理解。"""
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
        return UnderstandingOutput(
            narrative_structure=structure,
            emotional_curve=curve,
            key_hooks=hooks or ["前3秒给出核心卖点"],
        )
