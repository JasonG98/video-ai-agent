import sys
from loguru import logger
from app.config import get_settings


def configure_logging() -> None:
    """配置全局日志。"""
    settings = get_settings()
    logger.remove()
    logger.add(
        sys.stdout,
        level=settings.log_level.upper(),
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} - {message}",
        enqueue=True,
    )


__all__ = ["logger", "configure_logging"]
