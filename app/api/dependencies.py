from typing import Annotated

from fastapi import Depends, HTTPException, status

from app.models.users_model import Users
from ..core.database import SessionLocal
from ..core.security import decode_jwt
from fastapi.security import OAuth2PasswordBearer
from jose.exceptions import JWTError
from sqlalchemy.orm import Session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_auth_payload(token: Annotated[str, Depends(oauth2_scheme)]) -> dict:
    try:
        body = decode_jwt(token)
    except (JWTError, ValueError):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Could not validate credentials",
                            headers={"WWW-Authenticate": "Bearer"})
    return body

def require_authentication(auth_payload: Annotated[dict, Depends(get_auth_payload)]) -> None:
    if not auth_payload.get("sub") or auth_payload.get("type") != "access":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Could not validate credentials",
                            headers={"WWW-Authenticate": "Bearer"})

def get_current_user(auth_payload: Annotated[dict, Depends(get_auth_payload)],
                     _: Annotated[None, Depends(require_authentication)],
                     db: Annotated[Session, Depends(get_db)]) -> Users:
    user = db.query(Users).filter(Users.id == auth_payload.get("sub")).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user




