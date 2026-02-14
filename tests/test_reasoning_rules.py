from app.agent.reasoning import ReasoningLayer
from app.agent.schemas import PerceptionOutput, ShotSchema, UnderstandingOutput


def test_reasoning_layer_returns_recommendations() -> None:
    perception = PerceptionOutput(
        shots=[
            ShotSchema(index=0, start_time=0.0, end_time=5.0, duration=5.0, transcript="无CTA", objects=[], scene=""),
            ShotSchema(index=1, start_time=5.0, end_time=10.0, duration=5.0, transcript="无CTA", objects=[], scene=""),
        ],
        transcript_summary="",
    )
    understanding = UnderstandingOutput(narrative_structure={}, emotional_curve=[], key_hooks=[])
    result = ReasoningLayer().run(perception, understanding)
    assert len(result.recommendations) >= 1
    assert "avg_shot_duration" in result.rules_result
