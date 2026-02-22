from dataclasses import dataclass
import re


@dataclass(frozen=True)
class Email:
    value: str

    def __new__(cls, value: str):
        instance = super().__new__(cls)
        object.__setattr__(instance, "value", value.lower().strip())
        return instance

    def __post_init__(self):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", self.value):
            raise ValueError(f"Invalid email: {self.value}")
