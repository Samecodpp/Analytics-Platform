from typing import List

from ..repositories.projects_repo import ProjectRepository
from ..repositories.memberships_repo import MembershipRepository
from ..schemas.projects_schemas import ProjectCreate, ProjectResponse, ProjectsScope
from ..core.security import generate_api_key
from ..core.exceptions import AlreadyExistsError


class ProjectService:
    def __init__(self, project_repo: ProjectRepository, membership_repo: MembershipRepository):
        self.project_repo = project_repo
        self.membership_repo = membership_repo

    def create(self, user_id: int, payload: ProjectCreate) -> ProjectResponse:
        existing = self.project_repo.get_by_user_id(
            user_id=user_id,
            project_name=payload.name,
            role="owner",
        )
        if existing:
            raise AlreadyExistsError("Project with this name already exists")

        api_key = generate_api_key()
        payload_dict = payload.model_dump()
        payload_dict["api_key"] = api_key

        project = self.project_repo.create(payload_dict)

        self.membership_repo.create({
            "user_id": user_id,
            "project_id": project.id,
            "role": "owner",
            "is_invited": False,
            "invited_by": None,
        })

        self.project_repo.commit()
        return ProjectResponse.model_validate(project)

    def get_all(self, user_id: int, scope: ProjectsScope) -> List[ProjectResponse]:
        role = None
        if scope == ProjectsScope.OWN:
            role = "owner"
        elif scope == ProjectsScope.MEMBER:
            role = "viewer"

        projects = self.project_repo.get_by_user_id(
            user_id=user_id,
            project_name=None,
            role=role,
        )
        return [ProjectResponse.model_validate(p) for p in projects]
