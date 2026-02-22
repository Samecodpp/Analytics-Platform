from pydantic import BaseModel, EmailStr

from .base_schemas import BaseRegister


class RegisterRequest(BaseRegister):
    password: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str
