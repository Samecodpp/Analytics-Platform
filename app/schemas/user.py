from pydantic import BaseModel, EmailStr, field_validator, ConfigDict
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr

class UserCreds(UserBase):
    password: str

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





