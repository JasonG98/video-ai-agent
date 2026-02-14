from functools import lru_cache
from pathlib import Path
from urllib.parse import urlparse, urlunparse
from pydantic import Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


def _rewrite_service_host_to_localhost(url: str) -> str:
    """将 docker-compose 服务名地址改写为本机地址，便于本地 fastapi dev 调试。"""
    service_host_map = {
        "db": "127.0.0.1",
        "redis": "127.0.0.1",
        "minio": "127.0.0.1",
    }
    parsed = urlparse(url)
    host = parsed.hostname
    if not host:
        return url
    mapped_host = service_host_map.get(host)
    if not mapped_host:
        return url

    userinfo = ""
    if parsed.username:
        userinfo = parsed.username
        if parsed.password is not None:
            userinfo += f":{parsed.password}"
        userinfo += "@"
    port = f":{parsed.port}" if parsed.port else ""
    new_netloc = f"{userinfo}{mapped_host}{port}"
    return urlunparse(parsed._replace(netloc=new_netloc))


class Settings(BaseSettings):
    """应用配置。"""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "video_ai_agent"
    app_env: str = "dev"
    app_host: str = "0.0.0.0"
    app_port: int = 8000
    log_level: str = "INFO"

    database_url: str = Field(default="postgresql+psycopg://user:pass@db:5432/video_ai", alias="DB_URL")
    redis_url: str = Field(default="redis://redis:6379/0", alias="REDIS_URL")

    s3_endpoint: str = Field(default="http://minio:9000", alias="S3_ENDPOINT")
    s3_access_key: str = Field(default="minioadmin", alias="S3_ACCESS_KEY")
    s3_secret_key: str = Field(default="minioadmin", alias="S3_SECRET_KEY")
    s3_bucket: str = Field(default="videos", alias="DEFAULT_BUCKET")
    s3_region: str = "us-east-1"
    s3_secure: bool = False
    storage_backend: str = "minio"
    local_storage_path: str = "./storage"

    jwt_secret: str = Field(default="change_me", alias="JWT_SECRET")
    jwt_algorithm: str = "HS256"

    celery_broker_url: str | None = None
    celery_result_backend: str | None = None

    llm_provider: str = "mock"
    openai_api_key: str | None = None
    anthropic_api_key: str | None = None

    @model_validator(mode="after")
    def normalize_local_dev_hosts(self) -> "Settings":
        """
        在容器外本地开发时，自动把 compose 服务名地址映射到 localhost。
        这样 `fastapi dev app/main.py` 也能直接复用 `.env`。
        """
        if self.app_env != "dev" or Path("/.dockerenv").exists():
            return self
        self.database_url = _rewrite_service_host_to_localhost(self.database_url)
        self.redis_url = _rewrite_service_host_to_localhost(self.redis_url)
        self.s3_endpoint = _rewrite_service_host_to_localhost(self.s3_endpoint)
        return self

    @property
    def effective_celery_broker(self) -> str:
        return self.celery_broker_url or self.redis_url

    @property
    def effective_celery_backend(self) -> str:
        return self.celery_result_backend or self.redis_url


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
