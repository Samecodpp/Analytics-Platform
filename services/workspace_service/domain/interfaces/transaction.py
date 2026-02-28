from __future__ import annotations
from abc import ABC, abstractmethod

from .projects_repo import IProjectsRepository
from .members_repo import IMembersRepository
from .api_keys_repo import IApiKeyRepository


class ITransaction(ABC):
    projects: IProjectsRepository
    members: IMembersRepository
    api_keys: IApiKeyRepository

    @abstractmethod
    async def __aenter__(self) -> ITransaction: ...

    @abstractmethod
    async def __aexit__(self, exc_type, exc, tb) -> None: ...
