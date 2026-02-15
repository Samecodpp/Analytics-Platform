import pytest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime, timezone

from app.services.auth_service import AuthService
from app.schemas.auth_schemas import RegisterRequest
from app.core.exceptions import (
    AlreadyExistsError,
    InvalidCredentialsError,
    InvalidTokenError,
)

@pytest.fixture
def user_repo():
    mock = MagicMock()
    return mock


@pytest.fixture
def token_service():
    return Mock()


@pytest.fixture
def auth_service(user_repo, token_service):
    return AuthService(user_repo, token_service)


@pytest.fixture
def fake_user():
    user = Mock()
    user.id = 1
    user.email = "test@example.com"
    user.username = "testuser"
    user.first_name = None
    user.last_name = None
    user.hashed_password = "hashed_SecurePass123"
    user.created_at = datetime(2026, 1, 1, tzinfo=timezone.utc)
    return user

class TestRegister:
    @patch("app.services.auth_service.hash_password", return_value="hashed_pw")
    def test_register_success(self, mock_hash: Mock,
                              auth_service: AuthService,
                              user_repo: MagicMock,
                              fake_user: Mock) -> None:

        user_repo.get_by_email.return_value = None
        user_repo.create.return_value = fake_user

        creds = RegisterRequest(
            email="test@example.com",
            username="testuser",
            password="SecurePass123",
        )

        result = auth_service.register(creds)

        assert result.id == 1
        assert result.email == "test@example.com"
        assert result.username == "testuser"

        user_repo.get_by_email.assert_called_once_with("test@example.com")
        user_repo.create.assert_called_once()
        user_repo.commit.assert_called_once()

        mock_hash.assert_called_once_with("SecurePass123")

        create_arg = user_repo.create.call_args[0][0]
        assert "hashed_password" in create_arg
        assert "password" not in create_arg

    def test_register_email_already_exists(self,
                                           auth_service: AuthService,
                                           user_repo: MagicMock,
                                           fake_user: Mock
        ) -> None:
        user_repo.get_by_email.return_value = fake_user

        creds = RegisterRequest(
            email="test@example.com",
            username="testuser",
            password="SecurePass123",
        )

        with pytest.raises(AlreadyExistsError, match="already exists"):
            auth_service.register(creds)

        user_repo.create.assert_not_called()

    def test_register_password_validation(self) -> None:
        with pytest.raises(ValueError, match="at least 8 characters"):
            RegisterRequest(
                email="test@example.com",
                username="testuser",
                password="12345",
            )

class TestLogin:
    @patch("app.services.auth_service.verify_password", return_value=True)
    def test_login_success(self,
                           mock_verify: Mock,
                           auth_service: AuthService,
                           user_repo: MagicMock,
                           token_service: Mock,
                           fake_user: Mock
    ) -> None:
        user_repo.get_by_email.return_value = fake_user
        token_service.create_access_token.return_value = "access_token_123"
        token_service.create_refresh_token.return_value = "refresh_token_456"

        result = auth_service.login("test@example.com", "SecurePass123")

        assert result == {
            "access_token": "access_token_123",
            "refresh_token": "refresh_token_456",
        }

        mock_verify.assert_called_once_with("SecurePass123", fake_user.hashed_password)
        token_service.create_access_token.assert_called_once_with(fake_user.id)
        token_service.create_refresh_token.assert_called_once_with(fake_user.id)

    def test_login_user_not_found(self,
                                  auth_service: AuthService,
                                  user_repo: MagicMock
    ) -> None:
        user_repo.get_by_email.return_value = None
        with pytest.raises(InvalidCredentialsError, match="invalid"):
            auth_service.login("unknown@example.com", "SomePass123")

    @patch("app.services.auth_service.verify_password", return_value=False)
    def test_login_wrong_password(self,
                                  mock_verify: Mock,
                                  auth_service: AuthService,
                                  user_repo: MagicMock,
                                  fake_user: Mock
    ) -> None:
        user_repo.get_by_email.return_value = fake_user

        with pytest.raises(InvalidCredentialsError, match="invalid"):
            auth_service.login("test@example.com", "WrongPassword1")

        auth_service.token_service.create_access_token.assert_not_called()

class TestRefreshAccessToken:
    def test_refresh_success(self,
                             auth_service: AuthService,
                             token_service: Mock
    ) -> None:
        token_service.verify_refresh_token.return_value = {
            "sub": "1",
            "type": "refresh",
        }
        token_service.create_access_token.return_value = "new_access_token_789"

        result = auth_service.refresh_access_token("valid_refresh_token")

        assert result == "new_access_token_789"
        token_service.verify_refresh_token.assert_called_once_with(
            "valid_refresh_token"
        )
        token_service.create_access_token.assert_called_once_with(user_id="1")

    def test_refresh_token_is_none(self, auth_service: AuthService) -> None:
        with pytest.raises(InvalidTokenError, match="missing"):
            auth_service.refresh_access_token(None)

    def test_refresh_token_is_empty_string(self, auth_service: AuthService) -> None:
        with pytest.raises(InvalidTokenError, match="missing"):
            auth_service.refresh_access_token("")

    def test_refresh_token_expired(self, auth_service: AuthService, token_service: Mock) -> None:
        token_service.verify_refresh_token.side_effect = ValueError(
            "Refresh token expired"
        )

        with pytest.raises(InvalidTokenError, match="expired"):
            auth_service.refresh_access_token("expired_token")

    def test_refresh_token_invalid(self, auth_service: AuthService, token_service: Mock) -> None:
        token_service.verify_refresh_token.side_effect = ValueError(
            "Invalid refresh token"
        )

        with pytest.raises(InvalidTokenError, match="Invalid"):
            auth_service.refresh_access_token("garbage_token")
