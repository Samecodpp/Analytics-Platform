from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from ..dependencies import get_current_user, get_user_service, require_authentication
from ..schemas.user_schemas import User, UserUpdate
from ..services.user_service import UserService
from ..core.exceptions import NotFoundError

router = APIRouter(
    prefix="/users",
    dependencies=[Depends(require_authentication)],
    tags=["users"],
)


@router.get("/me", status_code=status.HTTP_200_OK, response_model=User)
def get_me(me: Annotated[User, Depends(get_current_user)]):
    return me


@router.patch("/me", status_code=status.HTTP_200_OK, response_model=User)
def update_me(
    me: Annotated[User, Depends(get_current_user)],
    payload: UserUpdate,
    user_service: Annotated[UserService, Depends(get_user_service)],
):
    try:
        return user_service.update_info(me.id, payload)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
