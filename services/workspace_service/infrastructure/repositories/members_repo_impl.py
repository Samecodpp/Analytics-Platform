from uuid import UUID
from sqlalchemy import select, delete, and_
from sqlalchemy.ext.asyncio import AsyncSession

from ...domain.interfaces import IMembersRepository
from ...domain.entities import Member
from ..models import MembersModel
from ..models.permissions_model import Permission as PermissionModel


class MembersRepository(IMembersRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create(self, member: Member) -> Member:
        model = self._to_model(member)
        self._session.add(model)
        await self._session.flush()

        await self._save_overrides(model.id, member)

        return await self.get_by_id(model.id)

    async def update(self, member: Member) -> Member | None:
        stmt = select(MembersModel).where(MembersModel.id == member.id)
        model = await self._session.scalar(stmt)

        model.role = member.role
        model.joined_at = member.joined_at

        await self._delete_overrides(member.id)
        await self._save_overrides(member.id, member)

        await self._session.flush()
        return await self.get_by_id(member.id)

    async def delete(self, id: UUID) -> None:
        stmt = delete(MembersModel).where(MembersModel.id == id)
        await self._session.execute(stmt)
        await self._session.flush()

    async def delete_all_by_project(self, project_id: UUID) -> None:
        stmt = delete(MembersModel).where(MembersModel.project_id == project_id)
        await self._session.execute(stmt)
        await self._session.flush()

    async def get_by_id(self, id: UUID) -> Member | None:
        stmt = select(MembersModel).where(MembersModel.id == id)
        model = await self._session.scalar(stmt)
        if not model:
            return None
        overrides = await self._load_overrides(model.id)
        return self._to_entity(model, overrides)

    async def get_by_project_user_id(
        self, project_id: UUID, user_id: UUID
    ) -> Member | None:
        stmt = select(MembersModel).where(
            and_(
                MembersModel.project_id == project_id,
                MembersModel.user_id == user_id,
            )
        )
        model = await self._session.scalar(stmt)
        if not model:
            return None
        overrides = await self._load_overrides(model.id)
        return self._to_entity(model, overrides)

    async def get_by_project_id(self, project_id: UUID) -> list[Member]:
        stmt = select(MembersModel).where(MembersModel.project_id == project_id)
        models = list(await self._session.scalars(stmt))

        if not models:
            return []

        member_ids = [m.id for m in models]
        overrides_stmt = select(PermissionModel).where(
            PermissionModel.member_id.in_(member_ids)
        )
        all_overrides = list(await self._session.scalars(overrides_stmt))

        overrides_map: dict[UUID, list[PermissionModel]] = {m.id: [] for m in models}
        for override in all_overrides:
            overrides_map[override.member_id].append(override)

        return [self._to_entity(m, overrides_map[m.id]) for m in models]

    async def exists(self, project_id: UUID, user_id: UUID) -> bool:
        stmt = select(MembersModel.id).where(
            and_(
                MembersModel.project_id == project_id,
                MembersModel.user_id == user_id,
            )
        )
        result = await self._session.scalar(stmt)
        return result is not None

    async def _load_overrides(self, member_id: UUID) -> list[PermissionModel]:
        stmt = select(PermissionModel).where(PermissionModel.member_id == member_id)
        result = await self._session.scalars(stmt)
        return list(result)

    async def _save_overrides(self, member_id: UUID, member: Member) -> None:
        for perm in member.granted_permissions:
            self._session.add(PermissionModel(
                member_id=member_id,
                permission=perm,
                granted=True,
                granted_by=member.invited_by or member.user_id,
            ))
        for perm in member.denied_permissions:
            self._session.add(PermissionModel(
                member_id=member_id,
                permission=perm,
                granted=False,
                granted_by=member.invited_by or member.user_id,
            ))
        await self._session.flush()

    async def _delete_overrides(self, member_id: UUID) -> None:
        stmt = delete(PermissionModel).where(PermissionModel.member_id == member_id)
        await self._session.execute(stmt)

    def _to_model(self, entity: Member) -> MembersModel:
        return MembersModel(
            id=entity.id,
            user_id=entity.user_id,
            project_id=entity.project_id,
            invited_by=entity.invited_by,
            role=entity.role,
            joined_at=entity.joined_at,
        )

    def _to_entity(
        self,
        model: MembersModel,
        overrides: list[PermissionModel],
    ) -> Member:
        return Member(
            id=model.id,
            user_id=model.user_id,
            project_id=model.project_id,
            invited_by=model.invited_by,
            role=model.role,
            joined_at=model.joined_at,
            created_at=model.created_at,
            granted_permissions={o.permission for o in overrides if o.granted},
            denied_permissions={o.permission for o in overrides if not o.granted},
        )
