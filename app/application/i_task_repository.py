from abc import ABC, abstractmethod
from domain import Task


class ITaskRepository(ABC):
    """
    タスクリポジトリを抽象化したインターフェース
    実際のDB(例: Firestore)の事情を隠蔽する

    Attributes
        add: タスクを追加するメソッド
    """

    @abstractmethod
    def add(self, task: Task) -> Task:
        pass
