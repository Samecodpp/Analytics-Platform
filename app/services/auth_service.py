from fastapi import HTTPException, Response, status
from sqlalchemy import or_
from sqlalchemy.orm import Session

from ..models.users_model import Users
from ..schemas.auth_schemas import RegisterRequest, Token
from ..core.security import hash_password, verify_password
from .token_service import TokenService


class AuthService:
    def __init__(self):
        self.token_service = TokenService()

    def register(self, db: Session, creds: RegisterRequest) -> Users:
        if db.query(Users).filter(creds.email == Users.email).first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this e-mail already registered!",
            )

        hashed_pwd = hash_password(creds.password)
        creds_dump = creds.model_dump(exclude={"password"})
        creds_dump["hashed_password"] = hashed_pwd

        user = Users(**creds_dump)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    def login(self, db: Session, username: str, password: str, response: Response) -> Token:
        user = db.query(Users).filter(
            or_(username == Users.email, username == Users.username)
        ).first()

        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Username/password is invalid!",
            )

        access_token = self.token_service.create_access_token(user.id)
        refresh_token = self.token_service.create_refresh_token(user.id)

        self.token_service.set_refresh_cookie(response, refresh_token)
        return Token(access_token=access_token)

    def refresh_access_token(self, refresh_token: str | None) -> Token:
        if not refresh_token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

        try:
            body = self.token_service.verify_refresh_token(refresh_token)
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))

        new_access_token = self.token_service.create_access_token(user_id=body["sub"])
        return Token(access_token=new_access_token)

    def logout(self, response: Response) -> None:
        self.token_service.delete_refresh_cookie(response)
