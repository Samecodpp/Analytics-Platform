from types import SimpleNamespace
from datetime import datetime, timezone


class FakeUserRepo:
    def __init__(self):
        self._users: dict[int, SimpleNamespace] = {}
        self._next_id = 1

    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False

    def commit(self):
        pass

    def get_by_email(self, email: str):
        return next((u for u in self._users.values() if u.email == email), None)

    def get_by_id(self, user_id: int):
        return self._users.get(user_id)

    def create(self, fields: dict):
        user = SimpleNamespace(
            id=self._next_id,
            created_at=datetime.now(timezone.utc),
            **fields,
        )
        self._users[self._next_id] = user
        self._next_id += 1
        return user

    def update_by_id(self, user_id: int, fields: dict):
        user = self._users.get(user_id)
        if not user:
            return None
        for k, v in fields.items():
            setattr(user, k, v)
        return user
