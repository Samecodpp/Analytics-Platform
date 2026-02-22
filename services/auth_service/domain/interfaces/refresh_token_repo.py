from abc import ABC, abstractmethod
from uuid import UUID

from ..entity.refresh_token import RefreshToken


class IRefreshTokenRepository(ABC):
    @abstractmethod
    async def create(self, refresh_token: RefreshToken) -> None: ...

    @abstractmethod
    async def revoke_by_id(self, id: UUID) -> bool: ...


