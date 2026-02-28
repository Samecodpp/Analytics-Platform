from abc import ABC, abstractmethod
from uuid import UUID

from ..entities import Project


class IProjectsRepository(ABC):

    @abstractmethod
    async def create(self, project: Project) -> Project: ...

    @abstractmethod
    async def update(self, project: Project) -> Project | None: ...

    @abstractmethod
    async def delete(self, slug: str) -> None: ...

    @abstractmethod
    async def get_by_id(self, id: UUID) -> Project | None: ...

    @abstractmethod
    async def get_by_slug(self, slug: str) -> Project | None: ...

    @abstractmethod
    async def get_all_by_owner(self, owner_id: UUID) -> list[Project]: ...

    @abstractmethod
    async def get_all_by_member(self, user_id: UUID) -> list[Project]: ...

    @abstractmethod
    async def get_all(self, user_id: UUID) -> list[Project]: ...
