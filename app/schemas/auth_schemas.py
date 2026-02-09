from typing import Literal
from datetime import datetime, timezone, timedelta
from uuid import uuid4
from pydantic import UUID4, BaseModel, EmailStr, model_serializer, field_validator

from ..core.config import settings

class RegisterRequest(BaseModel):
    email: EmailStr
    username: str
    password: str

    @field_validator("password")
    @classmethod
    def validate_password(cls, pwd: str) -> str:
        if len(pwd) < 8:
            raise ValueError("Password must be at least 8 characters long")
        return pwd

class JWTPayload(BaseModel):
    sub: str
    type: Literal["access", "refresh"]
    iat: datetime
    exp: datetime
    jti: UUID4 | None = None
    scope: str | None = None

    @classmethod
    def create_access_token(cls, user_id: int | str) -> JWTPayload:
        now = datetime.now(timezone.utc)
        return cls(
            sub=str(user_id),
            type="access",
            iat=now,
            exp=now+timedelta(seconds=settings.ACCESS_TOKEN_EXPIRE_SECONDS)
        )

    @classmethod
    def create_refresh_token(cls, user_id: int | str) -> JWTPayload:
        now = datetime.now(timezone.utc)
        return cls(
            sub=str(user_id),
            type="refresh",
            iat=now,
            exp=now+timedelta(seconds=settings.REFRESH_TOKEN_EXPIRE_SECONDS),
            jti=uuid4()
        )

    @model_serializer
    def serialize_model(self) -> dict:
        data = {
            "sub": self.sub,
            "type": self.type,
            "iat": int(self.iat.timestamp()),
            "exp": int(self.exp.timestamp()),
        }
        if self.jti is not None:
            data["jti"] = str(self.jti)
        if self.scope is not None:
            data["scope"] = self.scope
        return data


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

