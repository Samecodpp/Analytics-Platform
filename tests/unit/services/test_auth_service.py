import pytest
from pytest_mock import MockerFixture

from tests.fakes.fake_user_repo import FakeUserRepo
from tests.fakes.stubs import (
    StubTokenService,
    StubExpiredTokenService,
    StubInvalidTokenService,
)
from tests.factories import make_user
from app.services.auth_service import AuthService
from app.schemas.auth_schemas import RegisterRequest
from app.schemas.user_schemas import User
from app.core.exceptions import (
    AlreadyExistsError,
    InvalidCredentialsError,
    InvalidTokenError,
)

@pytest.fixture
def user_repo():
    return FakeUserRepo()


@pytest.fixture
def stub_token_service():
    return StubTokenService()


@pytest.fixture
def auth_service(user_repo, stub_token_service):
    return AuthService(user_repo, stub_token_service)

@pytest.mark.unit
class TestRegister:
    def test_register_success(self, user_repo: FakeUserRepo, mocker: MockerFixture):
        spy_commit = mocker.spy(user_repo, "commit")
        service = AuthService(
            user_repo, None
        )

        result = service.register(
            RegisterRequest(
                email="new@test.com",
                username="newuser",
                password="SecurePass123",
            )
        )

        assert isinstance(result, User)
        assert result.email == "new@test.com"
        assert result.username == "newuser"
        assert result.id is not None
        stored = user_repo.get_by_email("new@test.com")
        assert stored is not None
        assert stored.hashed_password != "SecurePass123"
        assert len(stored.hashed_password) > 20

        spy_commit.assert_called_once()

    def test_register_duplicate_email(self, user_repo: FakeUserRepo):
        service = AuthService(user_repo, None)

        service.register(
            RegisterRequest(
                email="dup@test.com", username="first", password="SecurePass123"
            )
        )

        with pytest.raises(AlreadyExistsError, match="already exists"):
            service.register(
                RegisterRequest(
                    email="dup@test.com", username="second", password="SecurePass123"
                )
            )

    def test_register_password_validation(self):
        with pytest.raises(ValueError, match="at least 8 characters"):
            RegisterRequest(
                email="test@test.com",
                username="testuser",
                password="12345",
            )

@pytest.mark.unit
class TestLogin:
    def _register_user(self, user_repo: FakeUserRepo, email: str, password: str):
        service = AuthService(user_repo, None)
        service.register(
            RegisterRequest(email=email, username="testuser", password=password)
        )

    def test_login_success(self, user_repo: FakeUserRepo, auth_service: AuthService):
        self._register_user(user_repo, "login@test.com", "SecurePass123")

        result = auth_service.login("login@test.com", "SecurePass123")

        assert "access_token" in result
        assert "refresh_token" in result
        assert result["access_token"] == "access_stub"
        assert result["refresh_token"] == "refresh_stub"

    def test_login_user_not_found(self, auth_service: AuthService):
        with pytest.raises(InvalidCredentialsError, match="Invalid credentials"):
            auth_service.login("unknown@test.com", "SomePass123")

    def test_login_wrong_password(
        self, user_repo: FakeUserRepo, auth_service: AuthService
    ):
        self._register_user(user_repo, "wrong@test.com", "CorrectPass123")

        with pytest.raises(InvalidCredentialsError, match="Invalid credentials"):
            auth_service.login("wrong@test.com", "WrongPassword1")

@pytest.mark.unit
class TestRefreshAccessToken:
    def test_refresh_success(self, auth_service: AuthService):
        result = auth_service.refresh_access_token("valid_refresh_token")

        assert result == "access_stub"

    def test_refresh_token_is_none(self):
        service = AuthService(FakeUserRepo(), StubTokenService())

        with pytest.raises(InvalidTokenError, match="missing"):
            service.refresh_access_token(None)

    def test_refresh_token_is_empty_string(self):
        service = AuthService(FakeUserRepo(), StubTokenService())

        with pytest.raises(InvalidTokenError, match="missing"):
            service.refresh_access_token("")

    def test_refresh_token_expired(self):
        service = AuthService(FakeUserRepo(), StubExpiredTokenService())

        with pytest.raises(InvalidTokenError, match="expired"):
            service.refresh_access_token("expired_token")

    def test_refresh_token_invalid(self):
        service = AuthService(FakeUserRepo(), StubInvalidTokenService())

        with pytest.raises(InvalidTokenError, match="Invalid"):
            service.refresh_access_token("garbage_token")
