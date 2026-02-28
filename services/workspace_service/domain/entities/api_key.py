from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class ApiKey:
    project_id: UUID | None
    created_by: UUID | None
    key_hash: str
    key_prefix: str
    key_raw: str | None
    name: str = "default"
    id: UUID | None = None
    is_active: bool = True
    expires_at: datetime | None = None
    last_used_at: datetime | None = None
    created_at: datetime | None = None
