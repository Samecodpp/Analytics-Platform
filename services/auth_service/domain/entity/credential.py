from dataclasses import dataclass, field
from uuid import UUID, uuid4

from ..value_objects import Email


@dataclass
class Credential:
    email: Email
    hashed_password: str
    is_active: bool = False
    id: UUID | None = field(default_factory=uuid4)
