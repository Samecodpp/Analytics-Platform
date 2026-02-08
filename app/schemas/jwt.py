from typing import Literal
from datetime import datetime, timezone, timedelta
from uuid import uuid4
from pydantic import UUID4, BaseModel

from ..core.config import settings

class JWTPayload(BaseModel):
    sub: str
    type: Literal["access", "refresh"]
    iat: datetime
    exp: datetime
    jti: UUID4 | None = None
    scope: str | None = None

    @classmethod
    def create_access_token(cls, user_id: int) -> JWTPayload:
        now = datetime.now(timezone.utc)
        return cls(
            sub=str(user_id),
            type="access",
            iat=now,
            exp=now+timedelta(seconds=settings.ACCESS_TOKEN_EXPIRE_SECONDS)
        )

    @classmethod
    def create_refresh_token(cls, user_id: int) -> JWTPayload:
        now = datetime.now(timezone.utc)
        return cls(
            sub=str(user_id),
            type="refresh",
            iat=now,
            exp=now+timedelta(seconds=settings.REFRESH_TOKEN_EXPIRE_SECONDS),
            jti=uuid4()
        )

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
