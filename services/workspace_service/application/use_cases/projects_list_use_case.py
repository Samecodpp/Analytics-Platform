from ...domain.interfaces import ITransaction
from ...domain.value_objects import ProjectValue
from ..dto import ProjectsListInput, ProjectsListOutput

class ProjectsListUseCase:
    def __init__(self, transaction: ITransaction):
        self._transaction = transaction

    async def execute(self, input: ProjectsListInput) -> ProjectsListOutput:
        async with self._transaction as tx:
            if input.scope == "own":
                projects = await tx.projects.get_all_by_owner(input.user_id)
            elif input.scope == "member":
                projects = await tx.projects.get_all_by_member(input.user_id)
            else:
                projects = await tx.projects.get_all(input.user_id)

        return ProjectsListOutput(
            user_id=input.user_id,
            projects=[ProjectValue(project.id, project.name, project.slug) for project in projects]
        )
