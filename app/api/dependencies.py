from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose.exceptions import JWTError
from sqlalchemy.orm import Session

from ..core.database import SessionLocal
from ..core.security import decode_jwt
from ..repositories.users_repo import UserRepository
from ..repositories.projects_repo import ProjectRepository
from ..repositories.memberships_repo import MembershipRepository
from ..services.auth_service import AuthService
from ..services.token_service import TokenService
from ..services.user_service import UserService
from ..services.project_service import ProjectService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_user_repository(db: Annotated[Session, Depends(get_db)]) -> UserRepository:
    return UserRepository(db)


def get_project_repository(db: Annotated[Session, Depends(get_db)]) -> ProjectRepository:
    return ProjectRepository(db)


def get_membership_repository(db: Annotated[Session, Depends(get_db)]) -> MembershipRepository:
    return MembershipRepository(db)

def get_auth_service(user_repo: Annotated[UserRepository, Depends(get_user_repository)]) -> AuthService:
    return AuthService(user_repo, TokenService())


def get_user_service(user_repo: Annotated[UserRepository, Depends(get_user_repository)]) -> UserService:
    return UserService(user_repo)

def get_project_service(project_repo: Annotated[ProjectRepository, Depends(get_project_repository)],
                        membership_repo: Annotated[MembershipRepository, Depends(get_membership_repository)]) -> ProjectService:
    return ProjectService(project_repo, membership_repo)

def get_auth_payload(token: Annotated[str, Depends(oauth2_scheme)]) -> dict:
    try:
        body = decode_jwt(token)
    except (JWTError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return body

def require_authentication(auth_payload: Annotated[dict, Depends(get_auth_payload)]) -> None:
    if not auth_payload.get("sub") or auth_payload.get("type") != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

def get_user_id(auth_payload: Annotated[dict, Depends(get_auth_payload)],
                _: Annotated[None, Depends(require_authentication)]) -> int:
    return int(auth_payload.get("sub"))

from ..core.exceptions import NotFoundError

def get_current_user(user_service: Annotated[UserService, Depends(get_user_service)],
                     auth_payload: Annotated[dict, Depends(get_auth_payload)],
                     _: Annotated[None, Depends(require_authentication)]):
    user_id = int(auth_payload.get("sub"))
    try:
        return user_service.get_by_id(user_id)
    except NotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
