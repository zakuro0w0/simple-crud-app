from .i_task_repository import ITaskRepository
from domain import Task


class TaskService:
    def __init__(self, repository: ITaskRepository):
        self.repository = repository

    def create_task(self, task: Task) -> Task:
        return self.repository.add(task)
