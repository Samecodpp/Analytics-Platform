from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str

    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_SECONDS: int
    REFRESH_TOKEN_EXPIRE_SECONDS: int

    DEBUG: bool = True

    model_config = SettingsConfigDict(env_file=".env")


def get_settings() -> Settings:
    return Settings()
