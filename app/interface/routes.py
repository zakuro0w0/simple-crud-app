from fastapi import APIRouter
from .models import TaskCreateIn
from application import TaskService
from domain import Task
from infrastructure import TaskRepository

router = APIRouter()


@router.post("/")
async def create_task(task: TaskCreateIn):
    service = TaskService(repository=TaskRepository())
    # TaskCreateInをTaskに変換してから渡す
    created_task = service.create_task(
        Task(title=task.title, description=task.description)
    )
    return created_task
