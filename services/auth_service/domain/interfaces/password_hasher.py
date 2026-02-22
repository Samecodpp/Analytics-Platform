from abc import ABC, abstractmethod

from ..value_objects import Password

class IPasswordHasher(ABC):
    @abstractmethod
    def hash(self, password: Password) -> str: ...

    @abstractmethod
    def verify(self, password: Password, hashed: str) -> bool: ...
