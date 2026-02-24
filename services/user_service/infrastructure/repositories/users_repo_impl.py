from sqlalchemy.ext.asyncio import AsyncSession


from ...domain.entity.user import User
from ...domain.interfaces.user_repo import IUsersRepository
from ..models.users_model import UsersModel

class UsersRepository(IUsersRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create(self, user: User) -> None:
        model = self._to_model(user)
        self._session.add(model)
        await self._session.flush()

    def _to_model(self, entity: User) -> UsersModel:
        return UsersModel(
            id=entity.id,
            email=entity.email,
            username=entity.username,
            is_active=entity.is_active
        )

    def _to_entity(self, model: UsersModel) -> User:
        return User(
            id=model.id,
            email=model.email,
            username=model.username,
            is_active=model.is_active
        )
