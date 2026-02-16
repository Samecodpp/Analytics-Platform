from ..repositories.users_repo import UserRepository
from ..schemas.auth_schemas import RegisterRequest
from ..schemas.user_schemas import User
from ..core.security import hash_password, verify_password
from ..core.exceptions import (
    AlreadyExistsError,
    InvalidCredentialsError,
    InvalidTokenError,
)
from .token_service import TokenService


class AuthService:
    def __init__(self, user_repo: UserRepository, token_service: TokenService):
        self.user_repo = user_repo
        self.token_service = token_service

    def register(self, creds: RegisterRequest) -> User:
        with self.user_repo:
            if self.user_repo.get_by_email(creds.email):
                raise AlreadyExistsError("User with this email already exists")

            hashed_pwd = hash_password(creds.password)
            creds_dump = creds.model_dump(exclude={"password"})
            creds_dump["hashed_password"] = hashed_pwd

            new_user = self.user_repo.create(creds_dump)
            self.user_repo.commit()
        return User.model_validate(new_user)

    def login(self, username: str, password: str) -> dict:
        with self.user_repo:
            user = self.user_repo.get_by_email(username)

        if not user or not verify_password(password, user.hashed_password):
            raise InvalidCredentialsError("Username/password is invalid")

        access_token = self.token_service.create_access_token(user.id)
        refresh_token = self.token_service.create_refresh_token(user.id)

        return {"access_token": access_token, "refresh_token": refresh_token}

    def refresh_access_token(self, refresh_token: str | None) -> str:
        if not refresh_token:
            raise InvalidTokenError("Refresh token is missing")

        try:
            body = self.token_service.verify_refresh_token(refresh_token)
        except ValueError as e:
            raise InvalidTokenError(str(e))

        new_access_token = self.token_service.create_access_token(user_id=body["sub"])
        return new_access_token
