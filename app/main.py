from fastapi import FastAPI
from .api import auth_api, users_api
from . import models

app = FastAPI()
app.include_router(auth_api.router)
app.include_router(users_api.router)

@app.get("/")
def root():
    return {"message": "Hello World"}
