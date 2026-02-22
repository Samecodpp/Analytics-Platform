from typing import Annotated
from fastapi import (
    APIRouter,
    Response,
    HTTPException,
    status,
    Cookie,
    Depends
)

from ...application.use_cases import (
    RegisterUseCase,
    LoginUseCase,
    LogoutUseCase,
    RefreshUseCase
)
from ...application.dto import (
    RegisterInput,
    LoginInput,
    LogoutInput,
    RefreshInput
)
from ...domain.value_objects import Email, Password
from ..schemas import (
    RegisterRequest,
    RegisterResponse,
    LoginRequest,
    LoginResponse,
    TokenResponse
)
from ..dependencies import (
    get_login_use_case,
    get_logout_use_case,
    get_register_use_case,
    get_refresh_use_case
)

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/register", status_code=status.HTTP_201_CREATED, response_model=RegisterResponse
)
async def register(
    request: RegisterRequest,
    use_case: Annotated[RegisterUseCase, Depends(get_register_use_case)],
):
    output = await use_case.execute(
        RegisterInput(
            email=Email(request.email),
            username=request.username,
            password=Password(request.password),
        )
    )

    return RegisterResponse(
        id=output.id, email=output.email.value, username=output.username
    )


@router.post(
    "/login",
    status_code=status.HTTP_200_OK,
    response_model=LoginResponse
)
async def login(
    request: LoginRequest,
    use_case: Annotated[LoginUseCase, Depends(get_login_use_case)],
    response: Response
):
    output = await use_case.execute(
        LoginInput(
            email=Email(request.email),
            password=Password(request.password)
        )
    )

    response.set_cookie(
        "refresh_token",
        output.refresh_token,
        httponly=True,
        secure=True,
        samesite="lax"
    )

    return LoginResponse(access_token=output.access_token)


@router.delete("/logout", status_code=status.HTTP_204_NO_CONTENT, response_model=None)
async def logout(
    refresh_token: Annotated[str | None, Cookie()],
    logout_use_case: Annotated[LogoutUseCase, Depends(get_logout_use_case)],
    response: Response
):
    await logout_use_case.execute(LogoutInput(refresh_token))
    response.delete_cookie(
        "refresh_token",
        httponly=True,
        secure=True,
        samesite="lax"
    )

@router.post("/refresh", status_code=status.HTTP_200_OK, response_model=TokenResponse)
async def refresh(
    refresh_token: Annotated[str | None, Cookie()],
    refresh_use_case: Annotated[RefreshUseCase, Depends(get_refresh_use_case)],
    response: Response
):
    output = await refresh_use_case.execute(RefreshInput(refresh_token))
    response.set_cookie(
        "refresh_token",
        output.refresh_token,
        httponly=True,
        secure=True,
        samesite="lax"
    )

    return TokenResponse(access_token=output.access_token)
