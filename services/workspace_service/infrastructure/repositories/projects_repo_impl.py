from uuid import UUID
from sqlalchemy import select, update, delete, and_
from sqlalchemy.ext.asyncio import AsyncSession

from ...domain.entities import Project
from ...domain.interfaces import IProjectsRepository
from ...domain.value_objects import Role, Slug
from ...application.exceptions import NotFoundError
from ..models import ProjectsModel, MembersModel


class ProjectsRepository(IProjectsRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create(self, project: Project) -> Project:
        model = self._to_model(project)
        self._session.add(model)
        await self._session.flush()
        return self._to_entity(model)

    async def get_by_slug(self, slug: str) -> Project | None:
        stmt = select(ProjectsModel).where(ProjectsModel.slug == slug)
        model = await self._session.scalar(stmt)
        return self._to_entity(model)

    async def get_by_id(self, id: UUID) -> Project | None:
        stmt = select(ProjectsModel).where(ProjectsModel.id == id)
        model = await self._session.scalar(stmt)
        return self._to_entity(model)

    async def get_all(self, user_id: UUID) -> list[Project]:
        stmt = select(ProjectsModel).join(MembersModel).where(
            MembersModel.user_id == user_id
        )
        models = await self._session.scalars(stmt)
        return [self._to_entity(model) for model in models]

    async def get_all_by_owner(self, owner_id: UUID) -> list[Project]:
        stmt = select(ProjectsModel).where(ProjectsModel.owner_id == owner_id)
        models = await self._session.scalars(stmt)
        return [self._to_entity(model) for model in models]

    async def get_all_by_member(self, user_id: UUID) -> list[Project]:
        stmt = select(ProjectsModel).join(MembersModel).where(
            and_(MembersModel.user_id == user_id,  MembersModel.role != Role.OWNER)
        )
        models = await self._session.scalars(stmt)
        return [self._to_entity(model) for model in models]

    async def update(self, project: Project) -> Project | None:
        stmt = select(ProjectsModel).where(ProjectsModel.id == project.id)
        model = await self._session.scalar(stmt)

        for attr in ["name", "slug", "description", "timezone"]:
            new_value = getattr(project, attr, None)
            if new_value is not None:
                setattr(model, attr, new_value)

        await self._session.flush()
        return self._to_entity(model)

    async def delete(self, slug: str) -> None:
        stmt = delete(ProjectsModel).where(ProjectsModel.slug == slug)
        await self._session.execute(stmt)

    def _to_model(self, entity: Project) -> ProjectsModel:
        return ProjectsModel(
            id=entity.id,
            owner_id=entity.owner_id,
            name=entity.name,
            slug=str(entity.slug.value),
            description=entity.description,
            timezone=entity.timezone,
            is_active=entity.is_active,
        )

    def _to_entity(self, model: ProjectsModel) -> Project:
        return Project(
            id=model.id,
            owner_id=model.owner_id,
            name=model.name,
            slug=Slug(model.slug),
            description=model.description,
            timezone=model.timezone,
            is_active=model.is_active,
            created_at=model.created_at,
        )
