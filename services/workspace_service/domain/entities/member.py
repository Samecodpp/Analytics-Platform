from dataclasses import dataclass, field
from uuid import UUID
from datetime import datetime

from ..value_objects import Role, EPermission


@dataclass
class Member:
    project_id: UUID
    user_id: UUID
    role: Role
    id: UUID | None = None
    invited_by: UUID | None = None
    granted_permissions: set[EPermission] = field(default_factory=set)
    denied_permissions: set[EPermission] = field(default_factory=set)
    joined_at: datetime | None = None
    created_at: datetime | None = None
