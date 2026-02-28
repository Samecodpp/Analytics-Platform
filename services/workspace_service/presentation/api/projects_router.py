from typing import Annotated
from uuid import UUID
from fastapi import (
    APIRouter,
    Depends,
    Path,
    Query,
    status,
)


from ...application.use_cases import (
    CreateProjectUseCase,
    UpdateProjectUseCase,
    ProjectsListUseCase,
    GetProjectUseCase
)
from ...application.dto import (
    CreateProjectInput,
    UpdateProjectInput,
    ProjectsListInput,
    GetProjectInput
)
from ..schemas.request_schemas import (
    CreateProjectRequest,
    UpdateProjectRequest,
    ProjectsListRequest
)
from ..schemas.response_schemas import (
    ProjectResponse,
    UpdateProjectResponse,
    ProjectsListResponse,
    ProjectShortResponse
)
from ..dependencies import (
    get_current_user_id,
    get_create_project_use_case as create_use_case,
    get_update_project_use_case as update_use_case,
    get_projects_list_use_case as list_use_case,
    get_project_use_case as get_use_case,

)

router = APIRouter(prefix="/projects", tags=["projects"])


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=ProjectResponse
)
async def create_project(
    request: CreateProjectRequest,
    user_id: Annotated[UUID, Depends(get_current_user_id)],
    create_use_case: Annotated[CreateProjectUseCase, Depends(create_use_case)]
):
    output = await create_use_case.execute(
        CreateProjectInput(
            name=request.name,
            owner_id=user_id,
            timezone=request.timezone,
            description=request.description
        )
    )

    return ProjectResponse(
        id=output.id,
        name=output.name,
        slug=output.slug,
        owner_id=output.owner_id,
        description=output.description,
        timezone=output.timezone,
        created_at=output.created_at
    )


@router.patch(
    "/{slug}",
    status_code=status.HTTP_200_OK,
    response_model=UpdateProjectResponse
)
async def update_project(
    slug: Annotated[str, Path()],
    request: UpdateProjectRequest,
    user_id: Annotated[UUID, Depends(get_current_user_id)],
    update_use_case: Annotated[UpdateProjectUseCase, Depends(update_use_case)]
):
    output = await update_use_case.execute(
        UpdateProjectInput(
            slug=slug,
            user_id=user_id,
            new_name=request.name,
            new_description=request.description,
            new_timezone=request.timezone
        )
    )

    return UpdateProjectResponse(
        id=output.id,
        name=output.name,
        slug=output.slug,
        description=output.description,
        timezone=output.timezone
    )


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=ProjectsListResponse
)
async def get_projects_list(
    user_id: Annotated[UUID, Depends(get_current_user_id)],
    list_use_case: Annotated[ProjectsListUseCase, Depends(list_use_case)],
    request: Annotated[ProjectsListRequest, Query()]
):
    output = await list_use_case.execute(
        ProjectsListInput(
            user_id=user_id,
            scope=request.scope
        )
    )

    return ProjectsListResponse(
        projects=[
            ProjectShortResponse(
                id=p.id,
                name=p.name,
                slug=p.slug,
            )
            for p in output.projects
        ]
    )

@router.get(
    "/{slug}",
    status_code=status.HTTP_200_OK,
    response_model=ProjectResponse
)
async def get_project(
    slug: Annotated[str, Path()],
    user_id: Annotated[UUID, Depends(get_current_user_id)],
    get_use_case: Annotated[GetProjectUseCase, Depends(get_use_case)]
):
    output = await get_use_case.execute(
        GetProjectInput(slug=slug, user_id=user_id)
    )

    return ProjectResponse(
        id=output.id,
        name=output.name,
        slug=output.slug,
        owner_id=output.owner_id,
        description=output.description,
        timezone=output.timezone,
        created_at=output.created_at
    )

