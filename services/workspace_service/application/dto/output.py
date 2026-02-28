from dataclasses import dataclass, field
from uuid import UUID
from datetime import datetime

from ...domain.value_objects import ProjectValue


@dataclass(frozen=True)
class CreateProjectOutput:
    id: UUID
    name: str
    slug: str
    owner_id: UUID
    description: str | None
    timezone: str
    created_at: datetime | None


@dataclass(frozen=True)
class ProjectsListOutput:
    user_id: UUID
    projects: list[ProjectValue] = field(default_factory=list)


@dataclass(frozen=True)
class UpdateProjectOutput:
    id: UUID
    name: str
    slug: str
    description: str | None
    timezone: str


@dataclass(frozen=True)
class CheckPermissionsOutput:
    user_id: UUID
    project_id: UUID
    access: bool


@dataclass(frozen=True)
class GenProjectOutput:
    api_key: str
    slug: str


@dataclass(frozen=True)
class GetProjectOutput(CreateProjectOutput):
    pass
