from app.agent.controller import VideoAnalysisAgent
from app.schemas.adaptation import ProductInfo


def test_analyze_and_adapt_generates_content() -> None:
    agent = VideoAnalysisAgent()
    product = ProductInfo(category="3C", name="降噪耳机", selling_points=["低延迟"], brand_tone="科技")
    result = agent.analyze_and_adapt("fake.mp4", new_product_info=product)
    assert "perception" in result
    assert "understanding" in result
    assert "reasoning" in result
    assert "generation" in result
    assert len(result["generation"]["adapted_script"]) > 0
