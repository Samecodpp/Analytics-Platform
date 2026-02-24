from ...application.dto.input import CreateUserInput
from ...application.use_cases import CreateUserUseCase

from ....shared.broker.events.register_event import RegisterEvent


class UserRegisterHandler:
    def __init__(self, create_user_use_case: CreateUserUseCase):
        self._create_user = create_user_use_case

    async def __call__(self, event: RegisterEvent) -> None:
        await self._create_user.execute(
            CreateUserInput(
                id=event.user_id,
                email=event.email,
                username=event.username
            )
        )
