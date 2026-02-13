from typing import Annotated
from fastapi import APIRouter, Cookie, Depends, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .dependencies import get_db
from ..schemas.auth_schemas import Token, RegisterRequest
from ..services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])
auth_service = AuthService()


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(creds: RegisterRequest, db: Annotated[Session, Depends(get_db)]):
    auth_service.register(db, creds)


@router.post("/login", status_code=status.HTTP_200_OK, response_model=Token)
def login(creds: Annotated[OAuth2PasswordRequestForm, Depends()],
          db: Annotated[Session, Depends(get_db)], response: Response):
    return auth_service.login(db, creds.username, creds.password, response)


@router.delete("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(response: Response):
    auth_service.logout(response)


@router.post("/refresh", status_code=status.HTTP_200_OK, response_model=Token)
def refresh_token(refresh_token: Annotated[str | None, Cookie()] = None):
    return auth_service.refresh_access_token(refresh_token)
