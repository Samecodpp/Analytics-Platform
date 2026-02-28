from ...domain.interfaces import ITransaction, IPolicyManager, IApiManager
from ...domain.value_objects import EPermission
from ...domain.entities import ApiKey
from ..dto import GenProjectInput, GenProjectOutput
from ..exceptions import NotFoundError, ForbbidenError


class GenApiKeyUseCase:
    def __init__(
        self,
        transaction: ITransaction,
        policy_manager: IPolicyManager,
        api_manager: IApiManager,
    ):
        self._transaction = transaction
        self._policy_manager = policy_manager
        self._api_manager = api_manager

    async def execute(self, input: GenProjectInput) -> GenProjectOutput:
        async with self._transaction as tx:
            member = await tx.members.get_by_user_and_slug(input.user_id, input.slug)

            if not member:
                raise NotFoundError(
                    f"Project '{input.slug}' not found or access denied"
                )

            if not self._policy_manager.can(
                member, EPermission.WORKSPACE_API_KEY_MANAGE
            ):
                raise ForbbidenError("Action forbidden")

            generated = self._api_manager.generate_key()

            await tx.api_keys.create(
                ApiKey(
                    project_id=member.project_id,
                    created_by=input.user_id,
                    key_hash=generated.key_hash,
                    key_prefix=generated.key_prefix,
                    key_raw=None,
                )
            )

        return GenProjectOutput(
            api_key=generated.key_raw,
            slug=input.slug,
        )
