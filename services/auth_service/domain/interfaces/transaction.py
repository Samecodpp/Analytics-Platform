from __future__ import annotations
from abc import ABC, abstractmethod

from .refresh_token_repo import IRefreshTokenRepository
from .credentials_repo import ICredentialsRepository


class ITransaction(ABC):
    credentials: ICredentialsRepository
    refresh_token: IRefreshTokenRepository

    @abstractmethod
    async def __aenter__(self) -> ITransaction: ...

    @abstractmethod
    async def __aexit__(self, exc_type, exc, tb) -> None: ...
