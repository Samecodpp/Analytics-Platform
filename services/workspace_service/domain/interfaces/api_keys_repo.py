from abc import ABC, abstractmethod
from uuid import UUID

from ..entities import ApiKey


class IApiKeysRepository(ABC):

    @abstractmethod
    async def create(self, api_key: ApiKey) -> ApiKey: ...

    @abstractmethod
    async def revoke(self, id: UUID) -> None: ...

    @abstractmethod
    async def get_by_id(self, id: UUID) -> ApiKey | None: ...

    @abstractmethod
    async def get_by_hash(self, key_hash: str) -> ApiKey | None: ...

    @abstractmethod
    async def get_all_by_project(self, project_id: UUID) -> list[ApiKey]: ...

    @abstractmethod
    async def update_last_used(self, id: UUID) -> None: ...

    @abstractmethod
    async def delete_all_by_project(self, project_id: UUID) -> None: ...
