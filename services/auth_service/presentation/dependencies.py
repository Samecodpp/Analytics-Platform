from typing import Annotated
from fastapi import Depends

from ..application.use_cases import (
    RegisterUseCase,
    LoginUseCase,
    LogoutUseCase,
    RefreshUseCase
)
from ..infrastructure.core.database import get_session_factory, async_sessionmaker
from ..infrastructure.core.settings import get_settings, Settings
from ..infrastructure.repositories import SQLAlchemyTransaction
from ..infrastructure.security import PwdHasher, JWTManager


def get_hasher() -> PwdHasher:
    return PwdHasher()


def get_jwt_manager(settings: Annotated[Settings, Depends(get_settings)]) -> JWTManager:
    return JWTManager(
        settings.SECRET_KEY,
        settings.ALGORITHM,
        settings.ACCESS_TOKEN_EXPIRE_SECONDS,
        settings.REFRESH_TOKEN_EXPIRE_SECONDS
    )


def get_transaction(
    session_factory: Annotated[async_sessionmaker, Depends(get_session_factory)]
) -> SQLAlchemyTransaction:
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
