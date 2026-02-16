from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_SECONDS: int
    REFRESH_TOKEN_EXPIRE_SECONDS: int
    DATABASE_URL: str

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
