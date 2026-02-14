
from ..repositories import UserRepository
from ..schemas.auth_schemas import RegisterRequest, Token
from ..schemas.user_schemas import User
from ..core.security import hash_password, verify_password
from .token_service import TokenService


class AuthService:
    def __init__(self):
        self.token_service = TokenService()

    def register(self, user_repo: UserRepository, creds: RegisterRequest) -> User:
        with user_repo:
            if user_repo.get_by_email(creds.email):
                raise "User with this email already exist" # TODO Own exception to this

            hashed_pwd = hash_password(creds.password)
            creds_dump = creds.model_dump(exclude={"password"})
            creds_dump["hashed_password"] = hashed_pwd

            new_user = user_repo.create(creds_dump)
            user_repo.commit()
        return User.model_validate(new_user)


    def login(self, user_repo: UserRepository, email: str, password: str) -> dict:
        with user_repo:
            user = user_repo.get_by_email(email)

        if not user or not verify_password(password, user.hashed_password):
            raise "Username/password is invalid!" # TODO Own exception to this

        access_token = self.token_service.create_access_token(user.id)
        refresh_token = self.token_service.create_refresh_token(user.id)

        return access_token, refresh_token

    def refresh_access_token(self, refresh_token: str | None) -> str:
        if not refresh_token:
            raise "Refresh token does not exist" # TODO Own exception to this

        try:
            body = self.token_service.verify_refresh_token(refresh_token)
        except ValueError as e:
            raise "Refresh token is invalid" # TODO Own exception to this

        new_access_token = self.token_service.create_access_token(user_id=body["sub"])
        return new_access_token
