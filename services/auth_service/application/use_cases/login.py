from ...domain.interfaces import IPasswordHasher, ITransaction, IJWTManager
from ...domain.entity import RefreshToken
from ..exceptions import NotFoundError, InvalidCredentialsError
from ..dto.input import LoginInput
from ..dto.output import LoginOutput


class LoginUseCase:
    def __init__(
        self,
        transaction: ITransaction,
        pwdhasher: IPasswordHasher,
        jwt_manager: IJWTManager
    ):
        self._transaction = transaction
        self._pwdhasher = pwdhasher
        self._jwt_manager = jwt_manager

    async def execute(self, input: LoginInput) -> LoginOutput:
        async with self._transaction as tx:
            creds = await tx.credentials.get_by_email(input.email.value)
            if not creds:
                raise NotFoundError("Not found credentials with this email")

            if not self._pwdhasher.verify(input.password, creds.hashed_password):
                raise InvalidCredentialsError("Invalid password")

            access_token = self._jwt_manager.create_access_token(creds.id)
            refresh_result = self._jwt_manager.create_refresh_token(creds.id)

            await tx.refresh_token.create(
                RefreshToken(
                    id=refresh_result.jti,
                    creds_id=creds.id,
                    expires_at=refresh_result.exp
                )
            )

        return LoginOutput(
            access_token=access_token,
            refresh_token=refresh_result.token
        )




