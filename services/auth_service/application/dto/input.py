from dataclasses import dataclass

from ...domain.value_objects import Email, Password


@dataclass(frozen=True)
class RegisterInput:
    email: Email
    username: str
    password: Password


@dataclass(frozen=True)
class LoginInput:
    email: Email
    password: Password


@dataclass(frozen=True)
class LogoutInput:
    refresh_token: str

@dataclass(frozen=True)
class RefreshInput(LogoutInput):
    pass
