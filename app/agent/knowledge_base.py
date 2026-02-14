class KnowledgeBase:
    """MVP 规则知识库。"""

    CTA_KEYWORDS = ["立即", "马上", "点击", "购买", "下单"]

    @staticmethod
    def has_cta(text: str) -> bool:
        return any(keyword in text for keyword in KnowledgeBase.CTA_KEYWORDS)
