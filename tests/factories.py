from faker import Faker
from types import SimpleNamespace
from datetime import timezone

from app.core.security import hash_password

faker = Faker()


def _apply_overrides(defaults: dict, overrides: dict) -> dict:
    for key, value in overrides.items():
        if value is ...:
            defaults.pop(key, None)
        else:
            defaults[key] = value
    return defaults


def make_user(**overrides) -> SimpleNamespace:
    password = overrides.pop("password", "TestPass123")
    defaults = {
        "id": faker.random_int(1, 9999),
        "email": faker.email(),
        "username": faker.user_name(),
        "first_name": None,
        "last_name": None,
        "hashed_password": hash_password(password),
        "created_at": faker.date_time(tzinfo=timezone.utc),
    }
    return SimpleNamespace(**_apply_overrides(defaults, overrides))


def make_project(**overrides) -> SimpleNamespace:
    defaults = {
        "id": faker.random_int(1, 9999),
        "name": faker.catch_phrase(),
        "description": faker.text(50),
        "api_key": faker.sha256()[:43],
        "created_at": faker.date_time(tzinfo=timezone.utc),
    }
    return SimpleNamespace(**_apply_overrides(defaults, overrides))
