from ...domain.interfaces import ITransaction, IPolicyManager
from ..dto import CheckPermissionsInput, CheckPermissionsOutput
from ..exceptions import NotFoundError


class CheckPermissionsUseCase:
    def __init__(self, transaction: ITransaction, policy_manager: IPolicyManager):
        self._transaction = transaction
        self._policy_manager = policy_manager

    async def execute(self, input: CheckPermissionsInput) -> CheckPermissionsOutput:
        async with self._transaction as tx:
            member = await tx.members.get_by_user_and_slug(input.user_id, input.slug)
            if not member:
                raise NotFoundError(
                    f"Project '{input.slug}' not found or access denied"
                )

        access = self._policy_manager.can_all(member, input.permissions)

        return CheckPermissionsOutput(
            user_id=member.user_id, project_id=member.project_id, access=access
        )
