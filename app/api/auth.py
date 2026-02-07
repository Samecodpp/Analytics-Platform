from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ..core.security import hash_password
from .dependencies import get_db
from app.models.users import Users
from ..schemas.user import UserRegister, UserResponse


router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def register(creds: UserRegister, db: Annotated[Session, Depends(get_db)]):
    if db.query(Users).filter(creds.email == Users.email).first():
        raise HTTPException(status_code=400, detail="User with this e-mail already registred!")

    hashed_pwd = hash_password(creds.password)
    creds_dump = creds.model_dump(exclude={"password"})
    creds_dump["hashed_password"] = hashed_pwd
    user = Users(**creds_dump)
    db.add(user)
    db.commit()
    db.refresh(user)

    return user

@router.post("/login", status_code=status.HTTP_201_CREATED)
def login(creds: Annotated[OAuth2PasswordRequestForm, Depends()],
          db: Annotated[Session, Depends(get_db)]):
    ###########################
    # TODO: REALIZE LOGIN LOGIC
    ###########################
    return {"acces_token": ..., "refresh_token": ..., "type_token": "bearer"}
