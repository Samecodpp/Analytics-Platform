from abc import ABC, abstractmethod
from uuid import UUID

from ..value_objects import JWTResult

class IJWTManager(ABC):
    @abstractmethod
    def create_access_token(self, sub: UUID) -> str: ...

    @abstractmethod
    def create_refresh_token(self, sub: UUID) -> JWTResult: ...

    @abstractmethod
    def verify(self, token: str) -> dict: ...
