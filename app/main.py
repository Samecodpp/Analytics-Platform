from fastapi import FastAPI
from .api import auth_api, users_api, projects_api
from .core import database

app = FastAPI(prefix="/api")
app.include_router(auth_api.router)
app.include_router(users_api.router)
app.include_router(projects_api.router)

database.Base.metadata.create_all(bind=database.engine)

@app.get("/")
def root():
    return {"message": "Hello World"}
