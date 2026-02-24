from abc import ABC, abstractmethod

from ..entity import User


class IUsersRepository(ABC):
    @abstractmethod
    async def create(self, user: User) -> None: ...
