from typing import Literal
from pydantic import BaseModel, Field

class CreateProjectRequest(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    timezone: str = Field(default="UTC", max_length=64)
    description: str = Field(default="", max_length=500)


class UpdateProjectRequest(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    description: str = Field(default="", max_length=500)
    timezone: str = Field(default="UTC", max_length=64)


class ProjectsListRequest(BaseModel):
    scope: Literal["own", "member", "all"] = "all"


class GenApiKeyRequest(BaseModel):
    name: str = Field(default="default", min_length=1, max_length=100)
