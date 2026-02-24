from dataclasses import dataclass
from uuid import UUID

from ..value_objects import Email

@dataclass
class User:
    id: UUID | None
    email: Email
    username: str | None
    is_active: bool = True

