from ...domain.interfaces import IJWTManager, ITransaction
from ..dto import LogoutInput
from ..exceptions import InvalidTokenError


class LogoutUseCase:
    def __init__(
        self,
        transaction: ITransaction,
        jwt_manager: IJWTManager
    ):
        self._transaction = transaction
        self._jwt_manager = jwt_manager

    async def execute(self, input: LogoutInput) -> None:
        payload = self._jwt_manager.verify(input.refresh_token)

        if payload["type"] != "refresh" or "jti" not in payload:
            raise InvalidTokenError("Invalid token")

        async with self._transaction as tx:
            await tx.refresh_token.revoke_by_id(payload["jti"])


