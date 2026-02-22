from pydantic import BaseModel, EmailStr


class BaseRegister(BaseModel):
    email: EmailStr
    username: str
