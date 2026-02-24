from ...domain.interfaces.transaction import ITransaction
from ...domain.entity import User
from ..dto.input import CreateUserInput

class CreateUserUseCase:
    def __init__(self, transaction: ITransaction):
        self._transaction = transaction

    async def execute(self, input: CreateUserInput) -> None:
        async with self._transaction as tx:
            await tx.user.create(
                User(
                    id=input.id,
                    email=input.email,
                    username=input.username
                )
            )
