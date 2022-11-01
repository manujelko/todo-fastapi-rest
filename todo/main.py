from fastapi import FastAPI

from . import models
from .company import companyapis
from .db import engine
from .routers import auth, todos

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(
    companyapis.router,
    prefix="/companyapis",
    tags=["companyapis"],
    responses={418: {"description": "Internal Use Only"}},
)
