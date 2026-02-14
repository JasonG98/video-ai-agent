from app.utils.prompt_builder import (
    build_copywriting_prompt,
    build_pattern_prompt,
    build_shot_adaptation_prompt,
    build_structure_prompt,
)


def test_prompt_builder_outputs_text() -> None:
    assert "结构" in build_structure_prompt("测试")
    assert "口播" in build_copywriting_prompt("产品A", "专业")
    assert "模板" in build_pattern_prompt(["建议1"])
    assert "改编" in build_shot_adaptation_prompt("镜头1", {"name": "产品A"})
