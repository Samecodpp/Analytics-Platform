from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update, func

from ...domain.entity.refresh_token import RefreshToken
from ...domain.interfaces import IRefreshTokenRepository
from ..models import RefreshTokenModel


class RefreshTokenRepository(IRefreshTokenRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create(self, refresh_token: RefreshToken) -> None:
        model = self._to_model(refresh_token)
        self._session.add(model)
        await self._session.flush()

    async def revoke_by_id(self, id: UUID) -> None:
        stmt = (
            update(RefreshTokenModel)
            .where(
                RefreshTokenModel.id == id,
                RefreshTokenModel.revoked_at.is_(None)
            )
            .values(revoked_at=func.now())
        )

        await self._session.execute(stmt)
        await self._session.flush()

    def _to_model(self, entity: RefreshToken) -> RefreshTokenModel:
        return RefreshTokenModel(
            id=entity.id, creds_id=entity.creds_id, expires_at=entity.expires_at
        )
