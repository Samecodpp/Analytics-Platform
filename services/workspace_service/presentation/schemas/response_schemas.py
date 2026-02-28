from uuid import UUID
from datetime import datetime
from pydantic import BaseModel

class ProjectResponse(BaseModel):
    id: UUID
    name: str
    slug: str
    owner_id: UUID
    description: str | None
    timezone: str
    created_at: datetime | None


class ProjectShortResponse(BaseModel):
    id: UUID
    name: str
    slug: str


class ProjectsListResponse(BaseModel):
    projects: list[ProjectShortResponse]


class UpdateProjectResponse(BaseModel):
    id: UUID
    name: str
    slug: str
    description: str | None
    timezone: str


class GenApiKeyResponse(BaseModel):
    api_key: str
    slug: str
