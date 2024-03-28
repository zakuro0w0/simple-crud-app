from application import TaskService
from domain import Task
from infrastructure import TaskRepositoryFirestore


class TaskController:
    """
    ユースケースとリポジトリの生成知識を隠蔽する。
    """

    def __init__(self):
        self.service = TaskService(repository=TaskRepositoryFirestore())

    def create_task(self, task: Task):
        """
        新しいタスクを作成します。

        Args:
            task (Task): 作成するタスクオブジェクト。

        Returns:
            Task: 作成されたタスクオブジェクト。
        """
        return self.service.create_task(task)
