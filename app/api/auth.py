from math import e
from typing import Annotated
from urllib import response
from fastapi import APIRouter, Cookie, Depends, HTTPException, status, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import or_
from sqlalchemy.orm import Session

from .dependencies import get_db
from ..schemas.jwt import JWTPayload, Token
from ..schemas.user import UserRegister, UserResponse
from ..core.security import create_jwt, decode_jwt
from app.models.users import Users
from ..core.security import hash_password, verify_password, get_cookie_refresh_config
from jose import ExpiredSignatureError, JWTError

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def register(creds: UserRegister, db: Annotated[Session, Depends(get_db)]):
    if db.query(Users).filter(creds.email == Users.email).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="User with this e-mail already registred!")

    hashed_pwd = hash_password(creds.password)
    creds_dump = creds.model_dump(exclude={"password"})
    creds_dump["hashed_password"] = hashed_pwd
    user = Users(**creds_dump)
    db.add(user)
    db.commit()
    db.refresh(user)

    return user

@router.post("/login", status_code=status.HTTP_200_OK, response_model=Token)
def login(creds: Annotated[OAuth2PasswordRequestForm, Depends()],
          db: Annotated[Session, Depends(get_db)], response: Response):

    user = db.query(Users).filter(
        or_(
            creds.username == Users.email,
            creds.username == Users.username
        )
    ).first()

    if not user or not verify_password(creds.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Username/password is invalid!")

    acces_token_payload = JWTPayload.create_access_token(user.id).model_dump()
    refresh_token_payload = JWTPayload.create_refresh_token(user.id).model_dump()

    access_token = create_jwt(acces_token_payload)
    refresh_token = create_jwt(refresh_token_payload)

    cookie_params = get_cookie_refresh_config()
    response.set_cookie("refresh_token", refresh_token, **cookie_params)
    return Token(access_token=access_token)

@router.post("/refresh", status_code=status.HTTP_200_OK, response_model=Token)
def refresh_token(refresh_token: Annotated[str | None, Cookie()] = None):
    if not refresh_token:
        raise HTTPException(status_code=401)

    try:
        body = decode_jwt(refresh_token)
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Refresh token expired")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    if body.get('type') != "refresh":
        raise HTTPException(status_code=401)

    payload = JWTPayload.create_access_token(user_id=body['sub']).model_dump()
    new_access_token = create_jwt(payload)

    return Token(access_token=new_access_token)
