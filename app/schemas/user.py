from pydantic import BaseModel, EmailStr, field_validator, ConfigDict
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr

class UserRegister(UserBase):
    password: str
    username: str | None = None
    first_name: str | None = None
    last_name: str | None = None

    @field_validator("password")
    @classmethod
    def validate_password(cls, pwd: str) -> str:
        if len(pwd) < 8:
            raise ValueError("Password must be at least 8 characters long")
        return pwd


class UserResponse(UserBase):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)





