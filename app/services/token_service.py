from jose import ExpiredSignatureError, JWTError

from ..schemas.auth_schemas import JWTPayload
from ..core.security import create_jwt, decode_jwt

class TokenService:
    @staticmethod
    def create_access_token(user_id: int | str) -> str:
        payload = JWTPayload.create_access_token(user_id).model_dump()
        return create_jwt(payload)

    @staticmethod
    def create_refresh_token(user_id: int | str) -> str:
        payload = JWTPayload.create_refresh_token(user_id).model_dump()
        return create_jwt(payload)

    @staticmethod
    def verify_refresh_token(token: str) -> dict:
        try:
            body = decode_jwt(token)
        except ExpiredSignatureError:
            raise ValueError("Refresh token expired")
        except JWTError:
            raise ValueError("Invalid refresh token")

        if body.get("type") != "refresh":
            raise ValueError("Token is not a refresh token")

        return body
