from dataclasses import dataclass
import re


@dataclass(frozen=True)
class Password:
    value: str

    def __post_init__(self):
        if len(self.value) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if not re.search(r"[a-z]", self.value):
            raise ValueError("Password must contain at least one lowercase letter")
        if not re.search(r"[A-Z]", self.value):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r"\d", self.value):
            raise ValueError("Password must contain at least one digit")
