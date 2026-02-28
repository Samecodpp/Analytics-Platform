from ...domain.interfaces import ITransaction, IPolicyManager
from ...domain.value_objects import EPermission
from ..dto import DeleteProjectInput
from ..exceptions import ForbbidenError, NotFoundError


class DeleteProjectUseCase:
    def __init__(self, transaction: ITransaction, policy_manager: IPolicyManager):
        self._transaction = transaction
        self._policy_manager = policy_manager

    async def execute(self, input: DeleteProjectInput) -> None:
        async with self._transaction as tx:
            member = await tx.members.get_by_user_and_slug(input.user_id, input.slug)

            if not member:
                raise NotFoundError(
                    f"Project '{input.slug}' not found or access denied"
                )
            if not self._policy_manager.can(member, EPermission.WORKSPACE_DELETE):
                raise ForbbidenError("This action is forbbiden")

            await tx.projects.delete(member.project_id)
