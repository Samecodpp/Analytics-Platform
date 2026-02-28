from ...domain.entities import Project
from ...domain.interfaces import ITransaction, IPolicyManager
from ...domain.value_objects import EPermission, Slug
from ..dto import UpdateProjectInput, UpdateProjectOutput
from ..exceptions import ForbbidenError, NotFoundError


class UpdateProjectUseCase:
    def __init__(self, transaction: ITransaction, policy_manager: IPolicyManager):
        self._transaction = transaction
        self._policy_manager = policy_manager

    async def execute(self, input: UpdateProjectInput) -> UpdateProjectOutput:
        async with self._transaction as tx:
            project = await tx.projects.get_by_slug(input.slug)
            if not project:
                raise NotFoundError(f"Project '{input.slug}' not found")

            member = await tx.members.get_by_project_user_id(project.id, input.user_id)
            if not member:
                raise NotFoundError(f"Project '{input.slug}' not found or access denied")

            if not self._policy_manager.can(member, EPermission.WORKSPACE_EDIT):
                raise ForbbidenError("This action is forbidden")

            updated = await tx.projects.update(
                Project(
                    id=project.id,
                    owner_id=project.owner_id,
                    name=input.new_name,
                    slug=Slug.from_name(input.new_name),
                    created_at=None,
                    description=input.new_description,
                    timezone=input.new_timezone,
                )
            )

        return UpdateProjectOutput(
            id=updated.id,
            name=updated.name,
            slug=updated.slug.value,
            description=updated.description,
            timezone=updated.timezone,
        )
