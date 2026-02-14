
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
                raise "User with this email already exist"  # TODO Own exception to this

            hashed_pwd = hash_password(creds.password)
            creds_dump = creds.model_dump(exclude={"password"})
            creds_dump["hashed_password"] = hashed_pwd

            new_user = user_repo.create(creds_dump)
            user_repo.commit()
        return User.model_validate(new_user)


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
