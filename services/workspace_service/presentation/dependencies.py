from typing import Annotated
from uuid import UUID
from fastapi import Depends, Header

from ..application.use_cases import *
from ..infrastructure.managers import PolicyManager, ApiKeysManager
from ..infrastructure.repositories import SQLAlchemyTransaction
from ..infrastructure.core.database import async_sessionmaker, get_session_factory


def get_api_manager() -> ApiKeysManager:
    return ApiKeysManager()


def get_policy_manager() -> PolicyManager:
    return PolicyManager()


async def get_current_user_id(
    x_user_id: UUID = Header(alias="X-User-Id")
) -> UUID:
    return x_user_id


def get_transaction(
    session_factory: Annotated[async_sessionmaker, Depends(get_session_factory)]
) -> SQLAlchemyTransaction:
    return SQLAlchemyTransaction(session_factory)


def get_create_project_use_case(
    transaction: Annotated[SQLAlchemyTransaction, Depends(get_transaction)]
) -> CreateProjectUseCase:
    return CreateProjectUseCase(transaction)


def get_update_project_use_case(
    transaction: Annotated[SQLAlchemyTransaction, Depends(get_transaction)],
    policy_manager: Annotated[PolicyManager, Depends(get_policy_manager)],
) -> UpdateProjectUseCase:
    return UpdateProjectUseCase(transaction, policy_manager)


def get_delete_project_use_case(
    transaction: Annotated[SQLAlchemyTransaction, Depends(get_transaction)],
    policy_manager: Annotated[PolicyManager, Depends(get_policy_manager)],
) -> DeleteProjectUseCase:
    return DeleteProjectUseCase(transaction, policy_manager)


def get_projects_list_use_case(
    transaction: Annotated[SQLAlchemyTransaction, Depends(get_transaction)],
) -> ProjectsListUseCase:
    return ProjectsListUseCase(transaction)


def get_gen_api_key_use_case(
    transaction: Annotated[SQLAlchemyTransaction, Depends(get_transaction)],
    policy_manager: Annotated[PolicyManager, Depends(get_policy_manager)],
    api_manager: Annotated[ApiKeysManager, Depends(get_api_manager)],
) -> GenApiKeyUseCase:
    return GenApiKeyUseCase(transaction, policy_manager, api_manager)


def get_check_permissions_use_case(
    transaction: Annotated[SQLAlchemyTransaction, Depends(get_transaction)],
    policy_manager: Annotated[PolicyManager, Depends(get_policy_manager)],
) -> CheckPermissionsUseCase:
    return CheckPermissionsUseCase(transaction, policy_manager)

def get_project_use_case(
    transaction: Annotated[SQLAlchemyTransaction, Depends(get_transaction)]
) -> GetProjectUseCase:
    return GetProjectUseCase(transaction)
