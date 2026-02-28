from abc import ABC, abstractmethod
from ..entities import Member
from ..value_objects import Permission

class IPolicyManager(ABC):

    @abstractmethod
    def can(self, member: Member, permission: Permission) -> bool: ...

    @abstractmethod
    def can_all(self, member: Member, permissions: set[Permission]) -> bool: ...

    @abstractmethod
    def allowed_permissions(self, member: Member) -> set[Permission]: ...
