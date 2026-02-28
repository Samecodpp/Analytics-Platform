from ...domain.interfaces import ITransaction
from ..dto import GetProjectInput, GetProjectOutput
from ..exceptions import NotFoundError, ForbbidenError

class GetProjectUseCase:
    def __init__(self, transaction: ITransaction):
        self._transaction = transaction

    async def execute(self, input: GetProjectInput) -> GetProjectOutput:
        async with self._transaction as tx:
            project = await tx.projects.get_by_slug(input.slug)

            if not project:
                raise NotFoundError(f"Do not found project {input.slug}")

            if not await tx.members.exists(project.id, input.user_id):
                raise ForbbidenError("You are not member of this project")

            return GetProjectOutput(
                id=project.id,
                name=project.name,
                slug=project.slug.value,
                owner_id=project.owner_id,
                description=project.description,
                timezone=project.timezone,
                created_at=project.created_at,
            )
