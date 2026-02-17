from types import SimpleNamespace
from datetime import datetime, timezone


class FakeProjectRepo:
    def __init__(self, membership_store: list | None = None):
        self._projects: dict[int, SimpleNamespace] = {}
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
        project = SimpleNamespace(
            id=self._next_id,
            created_at=datetime.now(timezone.utc),
            **fields,
        )
        self._projects[self._next_id] = project
        self._next_id += 1
        return project

    def get_by_user_id(
        self,
        user_id: int,
        project_name: str | None = None,
        role: str | None = None,
    ) -> list:
        result = []
        for m in self._memberships:
            if m.user_id != user_id:
                continue
            if role and m.role != role:
                continue
            project = self._projects.get(m.project_id)
            if not project:
                continue
            if project_name and project.name != project_name:
                continue
            result.append(project)
        return result

    def add_membership(self, user_id: int, project_id: int, role: str = "owner"):
        self._memberships.append(
            SimpleNamespace(
                user_id=user_id,
                project_id=project_id,
                role=role,
            )
        )
