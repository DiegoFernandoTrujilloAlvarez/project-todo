from typing import Annotated
from fastapi import APIRouter, HTTPException, Response, Depends
from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND, HTTP_200_OK, HTTP_204_NO_CONTENT
from ..schemas.tasks_schema import TaskRequest, TaskResponde, TaskUpdate
from ..services.tasks_service import TasksService
from app.config.dbconfig import get_db
from sqlalchemy.orm import Session
from ..models.user_model import Users
from ..utils.current_user import get_current_user
from fastapi.security import HTTPBearer

tasks = APIRouter(prefix="/tasks", tags=["tasks"])

@tasks.get("/", status_code=HTTP_200_OK, response_model=list[TaskResponde])
def get_tasks(current_user: Annotated[Users, Depends(get_current_user)], db: Session = Depends(get_db)):
    """Obtener la lista de tareas"""
    task_service = TasksService(db=db)
    return task_service.get_tasks()

@tasks.get("/{task_id}", status_code=HTTP_200_OK, response_model=TaskResponde)
def get_task_by_id(task_id: int, current_user: Annotated[Users, Depends(get_current_user)], db: Session = Depends(get_db)):
    """Obetener tarea por id"""
    task_service = TasksService(db=db)
    return task_service.get_task_by_id(task_id=task_id)

@tasks.post("/", status_code=HTTP_201_CREATED)
def create_task(user: TaskRequest, current_user: Annotated[Users, Depends(get_current_user)], db: Session = Depends(get_db)):
    task_service = TasksService(db=db)
    task_service.create_task(user)
    return Response(status_code=HTTP_201_CREATED)

@tasks.patch("/{task_id}", status_code=HTTP_200_OK)
def update_task(task_id: int, task_update: TaskUpdate, current_user: Annotated[Users, Depends(get_current_user)], db: Session = Depends(get_db)):
    task_service = TasksService(db=db)
    response = task_service.update_task(task_id=task_id, task_update=task_update)
    if not response:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Task not found")
    return Response(status_code=HTTP_200_OK)

@tasks.delete("/{task_id}", status_code=HTTP_204_NO_CONTENT)
def delete_task(task_id: int, current_user: Annotated[Users, Depends(get_current_user)], db: Session = Depends(get_db)):
    task_service = TasksService(db=db)
    response = task_service.delete_task(task_id=task_id)
    if not response:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Task not found")
