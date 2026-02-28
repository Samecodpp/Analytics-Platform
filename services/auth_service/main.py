from contextlib import asynccontextmanager
from fastapi import FastAPI


from auth_service.presentation.api.auth_router import router as auth_router
from auth_service.presentation.exception_handler import register_exception_handlers
from auth_service.infrastructure.core.database import init_engine, get_engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_engine()
    engine = get_engine()
    yield
    await engine.dispose()


app = FastAPI(lifespan=lifespan)
register_exception_handlers(app)
app.include_router(auth_router)

