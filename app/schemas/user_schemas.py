from datetime import datetime
from pydantic import BaseModel, EmailStr, ConfigDict


class UserBase(BaseModel):
    email: EmailStr


class UserMetaName(BaseModel):
    username: str | None = None
    first_name: str | None = None
    last_name: str | None = None


class User(UserBase, UserMetaName):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserUpdate(UserMetaName):
    pass
