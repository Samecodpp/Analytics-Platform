from typing import Annotated
from fastapi import Depends

from ..infrastructure.core.settings import get_settings
from ..infrastructure.core.database import create_engine, create_session_factory
from ..application.use_cases import (
    RegisterUseCase,
    LoginUseCase,
    LogoutUseCase,
    RefreshUseCase
)
from ..infrastructure.repositories import SQLAlchemyTransaction
from ..infrastructure.security import PwdHasher, JWTManager

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


def get_hasher() -> PwdHasher:
    return PwdHasher()


def get_jwt_manager() -> JWTManager:
    settings = get_settings()
    return JWTManager(
        settings.SECRET_KEY,
        settings.ALGORITHM,
        settings.ACCESS_TOKEN_EXPIRE_SECONDS,
        settings.REFRESH_TOKEN_EXPIRE_SECONDS
    )


def get_transaction() -> SQLAlchemyTransaction:
    session_factory = _get_session_factory()
    return SQLAlchemyTransaction(session_factory)


def get_register_use_case(
    transaction: Annotated[SQLAlchemyTransaction, Depends(get_transaction)],
    hasher: Annotated[PwdHasher, Depends(get_hasher)]
) -> RegisterUseCase:
    return RegisterUseCase(transaction, hasher)


def get_login_use_case(
    transaction: Annotated[SQLAlchemyTransaction, Depends(get_transaction)],
    hasher: Annotated[PwdHasher, Depends(get_hasher)],
    jwt_manager: Annotated[JWTManager, Depends(get_jwt_manager)]
) -> LoginUseCase:
    return LoginUseCase(transaction, hasher, jwt_manager)


def get_logout_use_case(
    transaction: Annotated[SQLAlchemyTransaction, Depends(get_transaction)],
    jwt_manager: Annotated[JWTManager, Depends(get_jwt_manager)]
) -> LogoutUseCase:
    return LogoutUseCase(transaction, jwt_manager)


def get_refresh_use_case(
    transaction: Annotated[SQLAlchemyTransaction, Depends(get_transaction)],
    jwt_manager: Annotated[JWTManager, Depends(get_jwt_manager)]
) -> RefreshUseCase:
    return RefreshUseCase(transaction, jwt_manager)
