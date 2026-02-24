from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
    AsyncEngine,
)
from sqlalchemy.orm import DeclarativeBase

from .settings import Settings


class Base(DeclarativeBase):
    pass


def create_engine(settings: Settings) -> AsyncEngine:
    return create_async_engine(
        settings.DATABASE_URL,
        echo=settings.DEBUG,
    )


def create_session_factory(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(
        engine,
        expire_on_commit=False,
    )


