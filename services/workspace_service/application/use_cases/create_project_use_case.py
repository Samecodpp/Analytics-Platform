from ...domain.interfaces import ITransaction
from ...domain.entities import Project, Member
from ...domain.value_objects import Slug, Role
from ..dto import CreateProjectInput, CreateProjectOutput


class CreateProjectUseCase:
    def __init__(self, transaction: ITransaction):
        self._transaction = transaction

    async def execute(self, input: CreateProjectInput) -> CreateProjectOutput:
        async with self._transaction as tx:
            project = await tx.projects.create(
                Project(
                    name=input.name,
                    owner_id=input.owner_id,
                    slug=Slug.from_name(input.name),
                    created_at=None,
                    timezone=input.timezone,
                    description=input.description,
                )
            )

            await tx.members.create(
                Member(
                    user_id=project.owner_id,
                    project_id=project.id,
                    role=Role.OWNER,
                )
            )

            return CreateProjectOutput(
                id=project.id,
                name=project.name,
                slug=project.slug.value,
                owner_id=project.owner_id,
                description=project.description,
                timezone=project.timezone,
                created_at=project.created_at,
            )
