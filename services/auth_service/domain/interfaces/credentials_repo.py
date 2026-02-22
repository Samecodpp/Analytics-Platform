from abc import ABC, abstractmethod

from ..entity import Credential

class ICredentialsRepository(ABC):
    @abstractmethod
    async def create(self, creds: Credential) -> Credential: ...

    @abstractmethod
    async def get_by_email(self, email: str) -> Credential: ...


