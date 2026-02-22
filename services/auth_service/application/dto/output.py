from dataclasses import dataclass
from uuid import UUID

from ...domain.value_objects import Email


@dataclass(frozen=True)
class RegisterOutput:
    id: UUID | None
    email: Email
    username: str


@dataclass(frozen=True)
class LoginOutput:
    access_token: str
    refresh_token: str


@dataclass(frozen=True)
class RefreshOutput(LoginOutput):
    pass
