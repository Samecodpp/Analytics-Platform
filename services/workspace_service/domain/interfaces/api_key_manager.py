from abc import ABC, abstractmethod

from ..entities.api_key import ApiKey

class IApiKeysManager(ABC):
    @abstractmethod
    def generate_key(self) -> ApiKey: ...

    @abstractmethod
    def revoke_key(self, key: ApiKey) -> ApiKey: ...
