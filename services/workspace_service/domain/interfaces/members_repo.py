from abc import ABC, abstractmethod
from uuid import UUID

from ..entities import Member


class IMembersRepository(ABC):

    @abstractmethod
    async def create(self, member: Member) -> Member: ...

    @abstractmethod
    async def update(self, member: Member) -> Member | None: ...

    @abstractmethod
    async def delete(self, id: UUID) -> None: ...

    @abstractmethod
    async def delete_all_by_project(self, project_id: UUID) -> None: ...

    @abstractmethod
    async def get_by_id(self, id: UUID) -> Member | None: ...

    @abstractmethod
    async def get_by_project_user_id(
        self, project_id: UUID, user_id: UUID
    ) -> Member | None: ...

    @abstractmethod
    async def get_by_project_id(self, project_id: UUID) -> list[Member]: ...

    @abstractmethod
    async def exists(self, project_id: UUID, user_id: UUID) -> bool: ...
