from typing import Annotated

from fastapi import APIRouter, Cookie, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordRequestForm

from .dependencies import get_auth_service
from ..schemas.auth_schemas import Token, RegisterRequest
from ..schemas.user_schemas import User
from ..services.auth_service import AuthService
from ..core.exceptions import AlreadyExistsError, InvalidCredentialsError, InvalidTokenError
from ..core.security import get_cookie_refresh_config

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=User)
def register(creds: RegisterRequest,
             auth_service: Annotated[AuthService, Depends(get_auth_service)]):
    try:
        return auth_service.register(creds)
    except AlreadyExistsError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.post("/login", status_code=status.HTTP_200_OK, response_model=Token)
def login(creds: Annotated[OAuth2PasswordRequestForm, Depends()],
          auth_service: Annotated[AuthService, Depends(get_auth_service)],
          response: Response):
    try:
        tokens = auth_service.login(creds.username, creds.password)
    except InvalidCredentialsError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))

    cookie_cfg = get_cookie_refresh_config()
    response.set_cookie(key="refresh_token", value=tokens["refresh_token"], **cookie_cfg)

    return Token(access_token=tokens["access_token"], token_type="bearer")


@router.delete("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(response: Response):
    response.delete_cookie("refresh_token", path="/")


@router.post("/refresh", status_code=status.HTTP_200_OK, response_model=Token)
def refresh_token(auth_service: Annotated[AuthService, Depends(get_auth_service)],
                  refresh_token: Annotated[str | None, Cookie()] = None):
    try:
        new_access = auth_service.refresh_access_token(refresh_token)
    except InvalidTokenError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))

    return Token(access_token=new_access, token_type="bearer")
