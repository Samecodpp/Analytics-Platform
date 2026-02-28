from dataclasses import dataclass
import re
import secrets
import string

BASE62_CHARS = string.digits + string.ascii_letters


def random_base62(n: int) -> str:
    return ''.join(secrets.choice(BASE62_CHARS) for _ in range(n))


@dataclass(frozen=True)
class Slug:
    value: str

    def __post_init__(self):
        if not re.match(r'^[a-z0-9][a-z0-9-]{1,48}[a-z0-9]$', self.value):
            raise ValueError(
                f"Invalid slug '{self.value}'. "
                "Only lowercase letters, digits and hyphens. "
                "Min 3, max 50 characters."
            )

    @classmethod
    def from_name(cls, name: str, unique_suffix: bool = True) -> "Slug":
        slug_base = name.lower()
        slug_base = re.sub(r'[^a-z0-9\s-]', '', slug_base)
        slug_base = re.sub(r'[\s_]+', '-', slug_base)
        slug_base = re.sub(r'-+', '-', slug_base)
        slug_base = slug_base.strip('-')

        if unique_suffix:
            suffix = random_base62(6)
            slug_base = f"{slug_base[:50 - 7]}-{suffix}"

        return cls(value=slug_base[:50])

