import json
import redis
from app.config import get_settings

settings = get_settings()


def get_redis_client() -> redis.Redis:
    return redis.Redis.from_url(settings.redis_url, decode_responses=True)


def get_json(key: str) -> dict | None:
    value = get_redis_client().get(key)
    return json.loads(value) if value else None


def set_json(key: str, data: dict, expire_seconds: int = 86400) -> None:
    get_redis_client().set(key, json.dumps(data, ensure_ascii=False), ex=expire_seconds)
