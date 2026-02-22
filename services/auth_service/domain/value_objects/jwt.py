from dataclasses import dataclass, field
from datetime import datetime
import time
from typing import Literal
from uuid import UUID, uuid4


@dataclass(frozen=True)
class JWTPayload:
    sub: UUID
    exp: int
    type: Literal["access", "refresh"]
    iat: int = field(default_factory=lambda: int(time.time()))
    jti: UUID = field(default_factory=uuid4)
    iss: str = field(default="auth-service")

    def is_access(self) -> bool:
        return self.type == "access"

    def is_expired(self) -> bool:
        return int(time.time()) > self.exp

    def to_dict(self) -> dict:
        return {
            "sub": str(self.sub),
            "exp": self.exp,
            "type": self.type,
            "iat": self.iat,
            "jti": str(self.jti),
            "iss": self.iss,
        }
    
@dataclass
class JWTResult:
    token: str
    jti: UUID
    exp: datetime
