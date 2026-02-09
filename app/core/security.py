from pwdlib import PasswordHash
from jose import jwt
from .config import settings

pwd_hash = PasswordHash.recommended()

def hash_password(password: str) -> str:
    return pwd_hash.hash(password)

def verify_password(password: str, hashed: str) -> bool:
    return pwd_hash.verify(password, hashed)

def create_jwt(payload: dict) -> str:
    return jwt.encode(payload, settings.SECRET_KEY, settings.ALGORITHM)

def decode_jwt(token: str) -> dict:
    return jwt.decode(token, settings.SECRET_KEY, settings.ALGORITHM)

def get_cookie_refresh_config() -> dict:
    return {
        "httponly": True,
        "secure": False,  # True для HTTPS в prod
        "samesite": "lax",
        "max_age": settings.REFRESH_TOKEN_EXPIRE_SECONDS,
        "path": "/"
    }

