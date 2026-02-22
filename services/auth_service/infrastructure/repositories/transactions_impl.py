from __future__ import annotations
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from ...domain.interfaces.transaction import ITransaction
from .credentials_repo_impl import CredentialsRepository
from .refresh_token_repo_impl import RefreshTokenRepository


class SQLAlchemyTransaction(ITransaction):
    def __init__(self, session_factory: async_sessionmaker):
        self._session_factory = session_factory

    async def __aenter__(self) -> SQLAlchemyTransaction:
        self._session: AsyncSession = self._session_factory()
        self.credentials = CredentialsRepository(self._session)
        self.refresh_token = RefreshTokenRepository(self._session)
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        if exc_type:
            await self._session.rollback()
        else:
            await self._session.commit()
        await self._session.close()
