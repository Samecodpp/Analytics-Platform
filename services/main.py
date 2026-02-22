from contextlib import asynccontextmanager

from fastapi import FastAPI

from .auth_service.infrastructure.core.database import create_engine
from .auth_service.infrastructure.core.settings import get_settings
from .auth_service.presentation.api.auth_router import router as auth_router
from .auth_service.presentation.exception_handler import register_exception_handlers


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    engine = create_engine(settings)
    yield
    await engine.dispose()


app = FastAPI(lifespan=lifespan)
register_exception_handlers(app)
app.include_router(auth_router)

