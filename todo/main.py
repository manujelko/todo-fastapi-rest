from typing import Optional

from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from . import models
from .db import SessionLocal, engine
from .routers import auth

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

HTTP_EXCEPTION = HTTPException(status_code=404, detail="Todo not found")

app.include_router(auth.router)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


class Todo(BaseModel):
    title: str
    description: Optional[str]
    priority: int = Field(gt=0, lt=6, description="The priority must be between 1-5")
    complete: bool


@app.delete("/{todo_id}")
async def delete_todo(
    todo_id: int, user: dict = Depends(auth.get_current_user), db: Session = Depends(get_db)
):
    if not user:
        raise auth.get_user_exception()

    todo_model = (
        db.query(models.Todos)
        .filter(models.Todos.id == todo_id)
        .filter(models.Todos.owner_id == user.get("id"))
        .first()
    )

    if not todo_model:
        raise HTTP_EXCEPTION

    db.query(models.Todos).filter(models.Todos.id == todo_id).delete()
    db.commit()
    return successful_response(200)


@app.put("/{todo_id}")
async def update_todo(
    todo_id: int,
    todo: Todo,
    user: dict = Depends(auth.get_current_user),
    db: Session = Depends(get_db),
):
    if not user:
        raise auth.get_user_exception()

    todo_model = (
        db.query(models.Todos)
        .filter(models.Todos.id == todo_id)
        .filter(models.Todos.owner_id == user.get("id"))
        .first()
    )

    if not todo_model:
        raise HTTP_EXCEPTION

    todo_model.title = todo.title
    todo_model.description = todo.description
    todo_model.priority = todo.priority
    todo_model.complete = todo.complete
    db.add(todo_model)
    db.commit()
    return successful_response(200)


@app.post("/")
async def create_todo(
    todo: Todo, user: dict = Depends(auth.get_current_user), db: Session = Depends(get_db)
):
    if not user:
        raise auth.get_user_exception()
    todo_model = models.Todos()
    todo_model.title = todo.title
    todo_model.description = todo.description
    todo_model.priority = todo.priority
    todo_model.complete = todo.complete
    todo_model.owner_id = user.get("id")
    db.add(todo_model)
    db.commit()
    return successful_response(201)


@app.get("/")
async def read_all(db: Session = Depends(get_db)):
    return db.query(models.Todos).all()


@app.get("/todo/user")
async def read_all_by_user(
    user: dict = Depends(auth.get_current_user), db: Session = Depends(get_db)
):
    if not user:
        raise auth.get_user_exception()
    return db.query(models.Todos).filter(models.Todos.owner_id == user.get("id")).all()


@app.get("/todo/{todo_id}")
async def read_todo(
    todo_id: int, user: dict = Depends(auth.get_current_user), db: Session = Depends(get_db)
):
    if not user:
        raise auth.get_user_exception()

    todo_model = (
        db.query(models.Todos)
        .filter(models.Todos.id == todo_id)
        .filter(models.Todos.owner_id == user.get("id"))
        .first()
    )

    if todo_model:
        return todo_model

    raise HTTP_EXCEPTION


def successful_response(status: int):
    return {"status": status, "transaction": "Successful"}
