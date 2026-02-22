from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ...domain.entity import Credential
from ...domain.value_objects import Email
from ...domain.interfaces import ICredentialsRepository
from ..models import CredentialsModel


class CredentialsRepository(ICredentialsRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create(self, creds: Credential) -> Credential:
        model = self._to_model(creds)
        self._session.add(model)
        await self._session.flush()
        return self._to_entity(model)

    async def get_by_email(self, email: str) -> Credential | None:
        result = await self._session.execute(
            select(CredentialsModel).where(CredentialsModel.email == email)
        )
        model = result.scalar_one_or_none()
        if not model:
            return None
        return self._to_entity(model)

    def _to_model(self, entity: Credential) -> CredentialsModel:
        return CredentialsModel(
            id=entity.id,
            email=entity.email.value,
            hashed_password=entity.hashed_password,
        )

    def _to_entity(self, model: CredentialsModel) -> Credential:
        return Credential(
            id=model.id,
            email=Email(model.email),
            hashed_password=model.hashed_password,
        )
