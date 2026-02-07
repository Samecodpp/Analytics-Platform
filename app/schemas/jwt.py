from typing import Literal
from datetime import datetime
from pydantic import BaseModel

class JWTPayload(BaseModel):
    sub: str
    type: Literal["access", "refresh"]
    iat: datetime
    exp: datetime
    jti: str | None
    scope: str | None
