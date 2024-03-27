from pydantic import BaseModel
from typing import NewType
from ..domain.task import Task


class TaskCreateIn(BaseModel):
    """
    タスクの入力モデルを表します。

    属性:
        title (str): タスクのタイトルです。
        description (str): タスクの説明です。
    """

    title: str
    description: str


TaskCreateOut = NewType("TaskCreateOut", Task)
