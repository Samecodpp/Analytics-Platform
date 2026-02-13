from fastapi import HTTPException, Response, status
from sqlalchemy import or_
from sqlalchemy.orm import Session

from ..models.users_model import Users
from ..schemas.auth_schemas import RegisterRequest, Token
from ..core.security import hash_password, verify_password
from .token_service import TokenService


class AuthService:
    """Service layer for authentication operations.

    Handles user registration, login, token refresh, and logout.
    Delegates token management to TokenService.
    """

    def __init__(self):
        self.token_service = TokenService()

    def register(self, db: Session, creds: RegisterRequest) -> Users:
        # """Register a new user with email and password.

        # Args:
        #     db: Database session
        #     creds: User registration credentials (email, username, password)

        # Returns:
        #     Created user object

        # Raises:
        #     HTTPException: If user with email already exists
        # """
        # # Check if user with this email already registered
        # if db.query(Users).filter(creds.email == Users.email).first():
        #     raise HTTPException(
        #         status_code=status.HTTP_400_BAD_REQUEST,
        #         detail="User with this e-mail already registered!",
        #     )

        # # Hash password and prepare user data
        # hashed_pwd = hash_password(creds.password)
        # creds_dump = creds.model_dump(exclude={"password"})
        # creds_dump["hashed_password"] = hashed_pwd

        # # Save user to database
        # user = Users(**creds_dump)
        # db.add(user)
        # db.commit()
        # db.refresh(user)
        # return user
        pass

    def login(self, db: Session, username: str, password: str, response: Response) -> Token:
        """Authenticate user and return access token with refresh token in cookie.

        Args:
            db: Database session
            username: User email or username
            password: User password
            response: HTTP response to set refresh token cookie

        Returns:
            Token object with access token

        Raises:
            HTTPException: If credentials are invalid
        """
        # Find user by email or username
        user = db.query(Users).filter(
            or_(username == Users.email, username == Users.username)
        ).first()

        # Verify password matches
        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Username/password is invalid!",
            )

        # Create tokens
        access_token = self.token_service.create_access_token(user.id)
        refresh_token = self.token_service.create_refresh_token(user.id)

        # Set refresh token in secure HTTP-only cookie
        self.token_service.set_refresh_cookie(response, refresh_token)
        return Token(access_token=access_token)

    def refresh_access_token(self, refresh_token: str | None) -> Token:
        """Generate new access token using valid refresh token.

        Args:
            refresh_token: Refresh token from cookie

        Returns:
            Token object with new access token

        Raises:
            HTTPException: If refresh token is missing or invalid
        """
        if not refresh_token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

        # Verify refresh token and extract user_id
        try:
            body = self.token_service.verify_refresh_token(refresh_token)
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))

        # Generate new access token from extracted user_id
        new_access_token = self.token_service.create_access_token(user_id=body["sub"])
        return Token(access_token=new_access_token)

    def logout(self, response: Response) -> None:
        """Remove refresh token cookie to invalidate user session.

        Args:
            response: HTTP response to clear refresh token cookie
        """
        self.token_service.delete_refresh_cookie(response)
