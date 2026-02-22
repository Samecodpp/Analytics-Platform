from uuid import UUID
from pydantic import BaseModel

from .base_schemas import BaseRegister

class RegisterResponse(BaseRegister):
    id: UUID


class LoginResponse(BaseModel):
    access_token: str
    type_token: str = "bearer"


class TokenResponse(LoginResponse):
    pass
