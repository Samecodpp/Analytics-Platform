from typing import Annotated
from fastapi import APIRouter, Depends, status
from ..schemas.user_schemas import User, UserUpdate
from ..models.users_model import Users
from .dependencies import get_db, require_authentication, get_current_user
from sqlalchemy.orm import Session

router = APIRouter(prefix="/users", dependencies=[Depends(require_authentication)], tags=["users"])

@router.get("/me", status_code=status.HTTP_200_OK, response_model=User)
def get_me(me: Annotated[User, Depends(get_current_user)]):
    return me

@router.patch("/me", status_code=status.HTTP_200_OK, response_model=User)
def update_me(me: Annotated[Users, Depends(get_current_user)],
              db: Annotated[Session, Depends(get_db)],
              payload: UserUpdate) -> User:

    update_data = payload.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        if hasattr(me, field):
            setattr(me, field, value)

    db.commit()
    db.refresh(me)

    return me



