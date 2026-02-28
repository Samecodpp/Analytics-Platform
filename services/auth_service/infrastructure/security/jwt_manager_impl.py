import time
from datetime import datetime, timezone
from uuid import UUID
import jwt

from ...domain.interfaces import IJWTManager
from ...domain.value_objects import JWTPayload, JWTResult


class JWTManager(IJWTManager):
    def __init__(self, secret: str, algorithm: str, access_timelife: int, refresh_timelife: int):
        self._secret = secret
        self._algorithm = algorithm
        self._access_timelife = access_timelife
        self._refresh_timelife = refresh_timelife

    def create_access_token(self, sub: UUID) -> str:
        payload_dict = JWTPayload(
            sub=sub,
            type="access",
            exp=int(time.time()) + self._access_timelife
        ).to_dict()

        return jwt.encode(payload_dict, self._secret, algorithm=self._algorithm)

    def create_refresh_token(self, sub: UUID) -> JWTResult:
        payload = JWTPayload(
            sub=sub,
            type="refresh",
            exp=int(time.time()) + self._refresh_timelife
        )
        token = jwt.encode(payload.to_dict(), self._secret, algorithm=self._algorithm)

        return JWTResult(
            token=token,
            jti=payload.jti,
            exp=datetime.fromtimestamp(payload.exp, tz=timezone.utc)
        )

    def verify(self, token: str) -> dict:
        return jwt.decode(token, self._secret, algorithms=[self._algorithm])
