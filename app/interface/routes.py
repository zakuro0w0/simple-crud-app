from fastapi import APIRouter
from .models import TaskCreateIn
from .controller import TaskController
from domain import Task

router = APIRouter()
controller = TaskController()


@router.post("")
async def create_task(task: TaskCreateIn):
    # TaskCreateInをTaskに変換してから渡す
    created_task = controller.create_task(
        Task(title=task.title, description=task.description)
    )
    return created_task
