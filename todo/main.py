from fastapi import FastAPI
from . import models
from .db import engine


app = FastAPI()

models.Base.metadata.create_all(bind=engine)


@app.get("/")
async def create_database():
    return {"Database": "Created"}
