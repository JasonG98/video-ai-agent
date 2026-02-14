from __future__ import annotations

from typing import Any

from app.config import get_settings
from app.utils.validators import validate_with_retry


class LLMClient:
    """统一 LLM 调用客户端（MVP 默认 mock，可平滑替换真实 provider）。"""

    def __init__(self, provider: str | None = None) -> None:
        settings = get_settings()
        self.provider = provider or settings.llm_provider
        self.settings = settings

    def _mock_value(self, schema: dict[str, Any], prompt: str) -> Any:
        """根据 JSON Schema 递归构造 mock 值，确保结构化输出可校验。"""
        schema_type = schema.get("type")
        if schema_type == "object":
            properties = schema.get("properties", {})
            required = schema.get("required", [])
            result: dict[str, Any] = {}
            for key, child_schema in properties.items():
                if key in required or key in {"summary", "items", "narrative_structure", "execution_docs", "metadata"}:
                    result[key] = self._mock_value(child_schema, prompt)
            return result
        if schema_type == "array":
            item_schema = schema.get("items", {"type": "string"})
            return [self._mock_value(item_schema, prompt)]
        if schema_type == "number":
            return 1.0
        if schema_type == "integer":
            return 1
        if schema_type == "boolean":
            return True
        return f"mock::{prompt[:60]}"

    def complete_structured(self, prompt: str, schema: dict[str, Any]) -> dict[str, Any]:
        """结构化输出接口。

        TODO:
        - openai: 接入 responses API + json schema response_format
        - anthropic: 接入 messages API + 工具调用/json mode
        """
        if self.provider == "mock":
            mock = self._mock_value(schema, prompt)
            if not isinstance(mock, dict):
                mock = {"result": mock}
            return validate_with_retry(mock, schema, retries=1)
        if self.provider == "openai":
            raise NotImplementedError("OpenAI provider TODO")
        if self.provider == "anthropic":
            raise NotImplementedError("Anthropic provider TODO")
        raise ValueError(f"unsupported provider: {self.provider}")
