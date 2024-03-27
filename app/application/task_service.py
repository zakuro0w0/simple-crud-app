from ..domain.task import Task
from ..infrastructure.task_repository import TaskRepository


class TaskService:
    def __init__(self, repository: TaskRepository):
        self.repository = repository

    def create_task(self, task: Task) -> Task:
        return self.repository.add(task)
