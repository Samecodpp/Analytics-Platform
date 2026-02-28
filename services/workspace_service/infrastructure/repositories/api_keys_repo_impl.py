from uuid import UUID
from datetime import datetime, timezone
from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from ...domain.interfaces import IApiKeysRepository
from ...domain.entities import ApiKey
from ..models import ApiKeyModel


class ApiKeysRepository(IApiKeysRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create(self, api_key: ApiKey) -> ApiKey:
        model = self._to_model(api_key)
        self._session.add(model)
        await self._session.flush()
        return self._to_entity(model)

    async def revoke(self, id: UUID) -> None:
        stmt = update(ApiKeyModel).where(ApiKeyModel.id == id).values(is_active=False)
        await self._session.execute(stmt)
        await self._session.flush()

    async def get_by_id(self, id: UUID) -> ApiKey | None:
        stmt = select(ApiKeyModel).where(ApiKeyModel.id == id)
        model = await self._session.scalar(stmt)
        return self._to_entity(model) if model else None

    async def get_by_hash(self, key_hash: str) -> ApiKey | None:
        stmt = select(ApiKeyModel).where(
            ApiKeyModel.key_hash == key_hash,
            ApiKeyModel.is_active == True,
        )
        model = await self._session.scalar(stmt)
        return self._to_entity(model) if model else None

    async def get_all_by_project(self, project_id: UUID) -> list[ApiKey]:
        stmt = select(ApiKeyModel).where(ApiKeyModel.project_id == project_id)
        models = await self._session.scalars(stmt)
        return [self._to_entity(m) for m in models]

    async def update_last_used(self, id: UUID) -> None:
        stmt = update(ApiKeyModel).where(ApiKeyModel.id == id).values(
            last_used_at=datetime.now(timezone.utc)
        )
        await self._session.execute(stmt)
        await self._session.flush()

    async def delete_all_by_project(self, project_id: UUID) -> None:
        stmt = delete(ApiKeyModel).where(ApiKeyModel.project_id == project_id)
        await self._session.execute(stmt)
        await self._session.flush()

    def _to_model(self, entity: ApiKey) -> ApiKeyModel:
        return ApiKeyModel(
            id=entity.id,
            project_id=entity.project_id,
            created_by=entity.created_by,
            name=entity.name,
            key_hash=entity.key_hash,
            key_prefix=entity.key_prefix,
            is_active=entity.is_active,
            expires_at=entity.expires_at,
        )

    def _to_entity(self, model: ApiKeyModel) -> ApiKey:
        return ApiKey(
            id=model.id,
            project_id=model.project_id,
            created_by=model.created_by,
            name=model.name,
            key_hash=model.key_hash,
            key_prefix=model.key_prefix,
            key_raw=None,
            is_active=model.is_active,
            expires_at=model.expires_at,
            last_used_at=model.last_used_at,
            created_at=model.created_at,
        )
