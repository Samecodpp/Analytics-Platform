from fastapi import FastAPI

from .presentation.api import projects_router

app = FastAPI()

app.include_router(projects_router.router)
