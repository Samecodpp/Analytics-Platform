from jose import jwt
from ..core.config import settings

def create_jwt(payload: dict) -> str:
    return jwt.encode(payload, settings.SECRET_KEY, settings.ALGORITHM)

def decode_jwt(token: str) -> dict:
    return jwt.decode(token, settings.SECRET_KEY, settings.ALGORITHM)
