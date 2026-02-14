from datetime import datetime, timedelta, timezone
import jwt
from app.config import get_settings


def create_access_token(subject: str, expires_minutes: int = 60) -> str:
    """生成简化 JWT。"""
    settings = get_settings()
    payload = {
        "sub": subject,
        "exp": datetime.now(tz=timezone.utc) + timedelta(minutes=expires_minutes),
    }
    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)
