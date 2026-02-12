from fastapi import Response
from jose import ExpiredSignatureError, JWTError

from ..schemas.auth_schemas import JWTPayload
from ..core.security import create_jwt, decode_jwt, get_cookie_refresh_config


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

    @staticmethod
    def set_refresh_cookie(response: Response, token: str) -> None:
        cookie_params = get_cookie_refresh_config()
        response.set_cookie("refresh_token", token, **cookie_params)

    @staticmethod
    def delete_refresh_cookie(response: Response) -> None:
        response.delete_cookie("refresh_token")
