from __future__ import annotations
from abc import ABC, abstractmethod

from .user_repo import IUsersRepository


class ITransaction(ABC):
    user: IUsersRepository

    @abstractmethod
    async def __aenter__(self) -> ITransaction: ...

    @abstractmethod
    async def __aexit__(self, exc_type, exc, tb) -> None: ...
