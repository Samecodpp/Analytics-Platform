from ...domain.interfaces import ITransaction, IJWTManager
from ...domain.entity import RefreshToken
from ..dto import RefreshInput, RefreshOutput
from ..exceptions import InvalidTokenError

class RefreshUseCase:
    def __init__(self, transaction: ITransaction, jwt_manager: IJWTManager):
        self._transaction = transaction
        self._jwt_manager = jwt_manager

    async def execute(self, input: RefreshInput) -> RefreshOutput:
        payload = self._jwt_manager.verify(input.refresh_token)

        if(
            payload.get("type") != "refresh"
            or "jti" not in payload
            or "sub" not in payload
        ):
            raise InvalidTokenError("Invalid token")

        sub = payload.get("sub", None)
        jti = payload.get("jti", None)

        new_access_toke = self._jwt_manager.create_access_token(sub)
        new_refresh_result = self._jwt_manager.create_refresh_token(sub)

        async with self._transaction as tx:
            tx.refresh_token.revoke_by_id(jti)
            tx.refresh_token.create(
                RefreshToken(
                    id=new_refresh_result.jti,
                    creds_id=sub,
                    expires_at=new_refresh_result.exp
                )
            )

        return RefreshOutput(
            access_token=new_access_toke,
            refresh_token=new_refresh_result.token
        )
