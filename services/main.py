from contextlib import asynccontextmanager
from typing import Annotated
from fastapi import Depends, FastAPI


from .shared.core.database import create_engine
from .shared.core.settings import get_settings
from .shared.broker.bus.event_bus_impl import event_bus
from .user_service.presentation.handlers.user_register_handler import UserRegisterHandler
from .user_service.application.use_cases.create_user_use_case import CreateUserUseCase
from .user_service.presentation.dependencies import get_create_user_use_case
from .auth_service.presentation.api.auth_router import router as auth_router
from .auth_service.presentation.exception_handler import register_exception_handlers


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    engine = create_engine(settings)

    handler = UserRegisterHandler(Annotated[CreateUserUseCase, Depends(get_create_user_use_case)])
    event_bus.subscribe("auth.user_registered", handler)
    yield
    await engine.dispose()


app = FastAPI(lifespan=lifespan)
register_exception_handlers(app)
app.include_router(auth_router)

