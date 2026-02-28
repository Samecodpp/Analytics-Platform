from dataclasses import dataclass
from uuid import UUID

from .slug import Slug


@dataclass(frozen=True)
class ProjectValue:
    id: UUID
    name: str
    slug: Slug
