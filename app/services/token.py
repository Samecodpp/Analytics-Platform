from uuid import uuid4
from datetime import datetime, timezone, timedelta
from jose import jwt

from ..schemas.jwt import JWTPayload
from ..core.config import settings

def create_access_token(user_id: str) -> str:
    now = datetime.now(timezone.utc)
    token_payload = JWTPayload(
        sub=user_id,
        type="access",
        iat=now,
        exp=now+timedelta(seconds=settings.ACCESS_TOKEN_EXPIRE_SECONDS)
    )

    token = jwt.encode(token_payload.model_dump(), settings.SECRET_KEY, settings.ALGORITHM)
    return token

def create_refresh_token(user_id: str) -> str:
    now = datetime.now(timezone.utc)
    token_payload = JWTPayload(
        sub=user_id,
        type="refresh",
        iat=now,
        exp=now+timedelta(seconds=settings.ACCESS_TOKEN_EXPIRE_SECONDS),
        jti=str(uuid4())
    )
    token = jwt.encode(token_payload.model_dump(), settings.SECRET_KEY, settings.ALGORITHM)
    return
