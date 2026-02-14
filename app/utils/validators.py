from typing import Any
from jsonschema import validate, ValidationError


def validate_with_retry(payload: dict[str, Any], schema: dict[str, Any], retries: int = 1) -> dict[str, Any]:
    """校验结构化输出并支持重试。"""
    err: Exception | None = None
    for _ in range(retries + 1):
        try:
            validate(instance=payload, schema=schema)
            return payload
        except ValidationError as exc:
            err = exc
    raise ValueError(f"schema validation failed: {err}")
