import pytest
from pytest_mock import MockerFixture
from jose import ExpiredSignatureError, JWTError

from app.services.token_service import TokenService


@pytest.mark.unit
class TestCreateAccessToken:
    def test_returns_jwt_string(self, mocker: MockerFixture):
        mocker.patch(
            "app.services.token_service.create_jwt", return_value="access.jwt.token"
        )

        token = TokenService.create_access_token(user_id=1)

        assert token == "access.jwt.token"
        assert isinstance(token, str)

@pytest.mark.unit
class TestCreateRefreshToken:
    def test_returns_jwt_string(self, mocker: MockerFixture):
        mocker.patch(
            "app.services.token_service.create_jwt", return_value="refresh.jwt.token"
        )

        token = TokenService.create_refresh_token(user_id=1)

        assert token == "refresh.jwt.token"
        assert isinstance(token, str)

@pytest.mark.unit
class TestVerifyRefreshToken:
    def test_valid_refresh_token(self, mocker: MockerFixture):
        mocker.patch(
            "app.services.token_service.decode_jwt",
            return_value={
                "sub": "1",
                "type": "refresh",
                "iat": 1234567890,
                "exp": 1234570890,
                "jti": "some-uuid",
            },
        )

        result = TokenService.verify_refresh_token("valid_token")

        assert result["type"] == "refresh"
        assert result["sub"] == "1"

    def test_expired_token(self, mocker: MockerFixture):
        mocker.patch(
            "app.services.token_service.decode_jwt",
            side_effect=ExpiredSignatureError,
        )

        with pytest.raises(ValueError, match="expired"):
            TokenService.verify_refresh_token("expired_token")

    def test_invalid_jwt(self, mocker: MockerFixture):
        mocker.patch(
            "app.services.token_service.decode_jwt",
            side_effect=JWTError,
        )

        with pytest.raises(ValueError, match="Invalid refresh token"):
            TokenService.verify_refresh_token("invalid_token")

    def test_wrong_token_type(self, mocker: MockerFixture):
        mocker.patch(
            "app.services.token_service.decode_jwt",
            return_value={
                "sub": "1",
                "type": "access",
                "iat": 1234567890,
                "exp": 1234570890,
            },
        )

        with pytest.raises(ValueError, match="not a refresh token"):
            TokenService.verify_refresh_token("access_token")
