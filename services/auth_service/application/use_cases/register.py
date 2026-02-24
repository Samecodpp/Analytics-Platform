from ...domain.entity import Credential
from ...domain.interfaces import ITransaction, IPasswordHasher
from ..exceptions import AlreadyExistsError
from ..dto import RegisterInput, RegisterOutput

from ....shared.broker.bus.event_bus import IEventBus
from ....shared.broker.events.register_event import RegisterEvent

class RegisterUseCase:
    def __init__(
        self,
        transaction: ITransaction,
        pwdhasher: IPasswordHasher,
        event_bus: IEventBus
    ):
        self._transaction = transaction
        self._pwdhasher = pwdhasher
        self._event_bus = event_bus

    async def execute(self, input: RegisterInput) -> RegisterOutput:
        async with self._transaction as tx:

            if await tx.credentials.get_by_email(input.email.value):
                raise AlreadyExistsError("This email already exists")

            hashed_pwd = self._pwdhasher.hash(input.password)
            creds = Credential(email=input.email, hashed_password=hashed_pwd)
            new_creds = await tx.credentials.create(creds)

        await self._event_bus.publish(
            RegisterEvent(
                user_id=new_creds.id,
                email=new_creds.email,
                username=input.username
            )
        )

        return RegisterOutput(
            id=new_creds.id,
            email=new_creds.email,
            username=input.username,
        )
