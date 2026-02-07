from fastapi import FastAPI
from .api import auth
from . import models

app = FastAPI()
app.include_router(auth.router)

@app.get("/")
def root():
    return {"message": "Hello World"}
