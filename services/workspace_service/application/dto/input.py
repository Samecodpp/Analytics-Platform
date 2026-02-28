from dataclasses import dataclass
from uuid import UUID
from typing import Literal

from ...domain.value_objects import EPermission


@dataclass(frozen=True)
class BaseInput:
    slug: str
    user_id: UUID


@dataclass(frozen=True)
class CheckPermissionsInput(BaseInput):
    permissions: set[EPermission]


@dataclass(frozen=True)
class CreateProjectInput:
    name: str
    owner_id: UUID
    timezone: str = "UTC"
    description: str = ""


@dataclass(frozen=True)
class ProjectsListInput:
    user_id: UUID
    scope: Literal["own", "member", "all"]


@dataclass(frozen=True)
class UpdateProjectInput(BaseInput):
    new_name: str
    new_description: str
    new_timezone: str


@dataclass(frozen=True)
class DeleteProjectInput(BaseInput):
    pass


@dataclass(frozen=True)
class GenProjectInput(BaseInput):
    pass


@dataclass(frozen=True)
class GetProjectInput(BaseInput):
    pass
