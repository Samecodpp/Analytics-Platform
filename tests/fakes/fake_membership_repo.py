from types import SimpleNamespace
from datetime import datetime, timezone


class FakeMembershipRepo:
    def __init__(self, membership_store: list | None = None):
        self._memberships: list[SimpleNamespace] = (
            membership_store if membership_store is not None else []
        )
        self._next_id = 1

    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False

    def commit(self):
        pass

    def create(self, fields: dict):
        membership = SimpleNamespace(
            id=self._next_id,
            created_at=datetime.now(timezone.utc),
            **fields,
        )
        self._memberships.append(membership)
        self._next_id += 1
        return membership

    def get_by_project_id(self, project_id: int) -> list:
        return [m for m in self._memberships if m.project_id == project_id]
