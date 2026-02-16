from datetime import datetime
import enum
from pydantic import BaseModel, ConfigDict


class ProjectsScope(str, enum.Enum):
    OWN = "own"
    MEMBER = "member"
    ALL = "all"


class ProjectBase(BaseModel):
    name: str
    description: str | None = None


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(BaseModel):
    name: str | None = None
    description: str | None = None


class ProjectResponse(ProjectBase):
    id: int
    api_key: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
