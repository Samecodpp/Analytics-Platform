from dataclasses import dataclass
from uuid import UUID
from datetime import datetime

from ..value_objects import Slug

@dataclass
class Project:
    name: str
    slug: Slug
    owner_id: UUID | None
    created_at: datetime | None
    id: UUID | None = None
    description: str | None = None
    timezone: str = "UTC"
    is_active: bool = True

