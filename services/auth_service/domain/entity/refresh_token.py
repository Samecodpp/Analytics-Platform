from dataclasses import dataclass, field
from uuid import UUID
from datetime import datetime


@dataclass
class RefreshToken:
    id: UUID | None
    creds_id: UUID | None
    expires_at: datetime
    revoked_at: datetime | None = field(default=None)
