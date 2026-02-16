from unittest.mock import Mock, patch
import pytest
from jose import ExpiredSignatureError, JWTError

from app.services.token_service import TokenService


class TestCreateAccessToken:
    @patch("app.services.token_service.create_jwt", return_value="accesstokenstr")
    @patch("app.services.token_service.JWTPayload.create_access_token")
    def test_create_access_token_success(
        self, mock_create_access_token: Mock, mock_create_jwt: Mock
    ) -> None:
        mock_payload_obj = Mock()
        mock_payload_obj.model_dump.return_value = {
            "sub": "1",
            "type": "access",
            "iat": 1234567890,
            "exp": 1234570890,
        }
        mock_create_access_token.return_value = mock_payload_obj

        token = TokenService.create_access_token(user_id=1)

        assert token == "accesstokenstr"
        mock_create_access_token.assert_called_once_with(1)
        mock_create_jwt.assert_called_once()
        mock_payload_obj.model_dump.assert_called_once()


class TestCreateRefreshToken:
    @patch("app.services.token_service.create_jwt", return_value="refreshtokenstr")
    @patch("app.services.token_service.JWTPayload.create_refresh_token")
    def test_create_refresh_token_success(
        self, mock_create_refresh_token: Mock, mock_create_jwt: Mock
    ) -> None:
        mock_payload_obj = Mock()
        mock_payload_obj.model_dump.return_value = {
            "sub": "1",
            "type": "access",
            "iat": 1234567890,
            "exp": 1234570890,
            "jti": "UUID",
        }
        mock_create_refresh_token.return_value = mock_payload_obj

        token = TokenService.create_refresh_token(1)

        assert token == "refreshtokenstr"
        mock_create_refresh_token.assert_called_once_with(1)
        mock_create_jwt.assert_called_once()
        mock_payload_obj.model_dump.assert_called_once()


class TestVerifyRefreshToken:
    @patch("app.services.token_service.decode_jwt")
    def test_verify_refresh_token_success(self, mock_decode: Mock) -> None:
        mock_decode.return_value = {
            "sub": "1",
            "type": "refresh",
            "iat": 1234567890,
            "exp": 1234570890,
            "jti": "UUID",
        }

        result = TokenService.verify_refresh_token("valid_token")

        assert result["type"] == "refresh"
        mock_decode.assert_called_once_with("valid_token")

    @patch("app.services.token_service.decode_jwt")
    def test_verify_refresh_token_expired(self, mock_decode: Mock) -> None:
        mock_decode.side_effect = ExpiredSignatureError

        with pytest.raises(ValueError, match="expired"):
            TokenService.verify_refresh_token("expired_token")

    @patch("app.services.token_service.decode_jwt")
    def test_verify_refresh_token_invalid_jwt(self, mock_decode: Mock) -> None:
        mock_decode.side_effect = JWTError

        with pytest.raises(ValueError, match="Invalid refresh token"):
            TokenService.verify_refresh_token("invalid_token")

    @patch("app.services.token_service.decode_jwt")
    def test_verify_refresh_token_wrong_type(self, mock_decode: Mock) -> None:
        mock_decode.return_value = {
            "sub": "1",
            "type": "access",
            "iat": 1234567890,
            "exp": 1234570890,
            "jti": "UUID",
        }

        with pytest.raises(ValueError, match="not a refresh token"):
            TokenService.verify_refresh_token("access_token")
