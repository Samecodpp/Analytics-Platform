from ...domain.interfaces import IPolicyManager
from ...domain.entities import Member
from ...domain.value_objects import EPermission, ROLE_PERMISSIONS


class PolicyManager(IPolicyManager):

    def allowed_permissions(self, member: Member) -> set[EPermission]:
        base = ROLE_PERMISSIONS.get(member.role, set()).copy()
        base |= member.granted_permissions
        base -= member.denied_permissions
        return base

    def can(self, member: Member, permission: EPermission) -> bool:
        return permission in self.allowed_permissions(member)

    def can_all(self, member: Member, permissions: set[EPermission]) -> bool:
        allowed = self.allowed_permissions(member)
        return all(p in allowed for p in permissions)
