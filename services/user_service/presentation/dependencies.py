from typing import Annotated

from fastapi import Depends

from ..application.use_cases.create_user_use_case import CreateUserUseCase
from ..infrastructure.repositories.transactions_impl import SQLAlchemyTransaction
from ...shared.core.settings import get_settings
from ...shared.core.database import create_engine, create_session_factory


_engine = None
_session_factory = None


def _get_engine():
    global _engine
    if _engine is None:
        settings = get_settings()
        _engine = create_engine(settings)
    return _engine


def _get_session_factory():
    global _session_factory
    if _session_factory is None:
        engine = _get_engine()
        _session_factory = create_session_factory(engine)
    return _session_factory


def get_transaction() -> SQLAlchemyTransaction:
    session_factory = _get_session_factory()
    return SQLAlchemyTransaction(session_factory)


def get_create_user_use_case(
    transaction: Annotated[SQLAlchemyTransaction, Depends(get_transaction)]
) -> CreateUserUseCase:
    return CreateUserUseCase(transaction)
