from typing import Annotated, List, Literal
from fastapi import APIRouter, HTTPException, status, Query, Depends
from sqlalchemy.orm import Session

from app.core.security import generate_api_key
from .dependencies import get_current_user, require_authentication, get_user_id, get_db
from ..schemas.projects_schemas import ProjectResponse, ProjectCreate, ProjectsScope
from ..schemas import User
from ..models import Projects, Memberships
from ..models.membership_model import Memberships, ProjectRole

router = APIRouter(prefix="/projects",
                   dependencies=[Depends(require_authentication)],
                   tags=["projects"])

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ProjectResponse)
def create_project(db: Annotated[Session, Depends(get_db)],
                   user: Annotated[User, Depends(get_current_user)],
                   payload: ProjectCreate):
    existing = db.query(Projects)\
        .join(Memberships)\
        .filter(
            Memberships.user_id == user.id,
            Projects.name == payload.name,
            Memberships.role == ProjectRole.OWNER
        ).first()

    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Project with this name has already exist!")

    api_key = generate_api_key()
    payload_dict = payload.model_dump()
    payload_dict.update(api_key=api_key)
    new_project = Projects(**payload_dict)

    db.add(new_project)
    db.flush()

    membership = Memberships(user_id=user.id,
                            project_id=new_project.id,
                            role=ProjectRole.OWNER,
                            is_invited=False,
                            invited_by=None)

    db.add(membership)
    db.commit()

    db.refresh(membership)
    db.refresh(new_project)
    return new_project

@router.get("/", status_code=status.HTTP_200_OK, response_model=List[ProjectResponse])
def get_projects(user_id: Annotated[int, Depends(get_user_id)],
                 db: Annotated[Session, Depends(get_db)],
                 scope: Annotated[ProjectsScope, Query()] = ProjectsScope.ALL):

    query = db.query(Projects).join(Memberships).filter(Memberships.user_id == user_id)

    if scope == ProjectsScope.OWN:
        query = query.filter(Memberships.role == ProjectRole.OWNER)
    elif scope == ProjectsScope.MEMBER:
        query = query.filter(Memberships.role != ProjectRole.OWNER)

    return query.all()
