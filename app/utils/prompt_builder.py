def build_structure_prompt(video_summary: str) -> str:
    return f"请分析该视频结构并输出开场-主体-结尾: {video_summary}"


def build_copywriting_prompt(product_name: str, tone: str) -> str:
    return f"请生成{tone}风格的{product_name}短视频口播文案"


def build_pattern_prompt(recommendations: list[str]) -> str:
    return f"根据建议抽象爆款模板: {'; '.join(recommendations)}"


def build_shot_adaptation_prompt(shot_summary: str, product_info: dict) -> str:
    return f"将镜头“{shot_summary}”改编为商品 {product_info.get('name')} 的版本"
