from infrastructure import TaskRepository
from domain import Task


class TaskService:
    def __init__(self, repository: TaskRepository):
        self.repository = repository

    def create_task(self, task: Task) -> Task:
        return self.repository.add(task)
