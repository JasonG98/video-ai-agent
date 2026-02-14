from typing import Any
from app.config import get_settings
from app.utils.validators import validate_with_retry


class LLMClient:
    def __init__(self, provider: str | None = None) -> None:
        settings = get_settings()
        self.provider = provider or settings.llm_provider
        self.settings = settings

    def complete_structured(self, prompt: str, schema: dict[str, Any]) -> dict[str, Any]:
        """结构化输出接口，MVP 默认 mock。"""
        if self.provider == "mock":
            mock = {"summary": prompt[:80], "items": ["mock_item"]}
            return validate_with_retry(mock, schema, retries=1)
        if self.provider == "openai":
            # TODO: 接入 OpenAI SDK
            raise NotImplementedError("OpenAI provider TODO")
        if self.provider == "anthropic":
            # TODO: 接入 Anthropic SDK
            raise NotImplementedError("Anthropic provider TODO")
        raise ValueError(f"unsupported provider: {self.provider}")
