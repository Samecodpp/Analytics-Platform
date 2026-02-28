from dataclasses import dataclass
from uuid import UUID
from datetime import datetime

from ..value_objects import EPermission


@dataclass
class Permission:
    project_id: UUID
    user_id: UUID
    permission: EPermission
    granted: bool
    granted_by: UUID
    id: UUID | None = None
    created_at: datetime | None = None
