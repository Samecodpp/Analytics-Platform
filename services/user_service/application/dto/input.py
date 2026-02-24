from dataclasses import dataclass
from uuid import UUID

from ...domain.value_objects.email import Email


@dataclass(frozen=True)
class CreateUserInput:
    id: UUID
    email: Email
    username: str
