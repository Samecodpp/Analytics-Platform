from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, Query, status

from ..dependencies import get_current_user, get_project_service, require_authentication
from ..schemas.projects_schemas import ProjectResponse, ProjectCreate, ProjectsScope
from ..schemas.user_schemas import User
from ..services.project_service import ProjectService
from ..core.exceptions import AlreadyExistsError

router = APIRouter(
    prefix="/projects",
    dependencies=[Depends(require_authentication)],
    tags=["projects"],
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ProjectResponse)
def create_project(user: Annotated[User, Depends(get_current_user)],
                   payload: ProjectCreate,
                   project_service: Annotated[ProjectService, Depends(get_project_service)]):
    try:
        return project_service.create(user.id, payload)
    except AlreadyExistsError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[ProjectResponse])
def get_projects(user: Annotated[User, Depends(get_current_user)],
                 project_service: Annotated[ProjectService, Depends(get_project_service)],
                 scope: Annotated[ProjectsScope, Query()] = ProjectsScope.ALL):
    return project_service.get_all(user.id, scope)
