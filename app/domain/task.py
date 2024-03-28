from pydantic import BaseModel, Field
from datetime import datetime


class Task(BaseModel):
    """
    タスクモデル。

    属性:
    title: str - タスクのタイトル。
    description: str - タスクの説明。
    completed: bool - タスクの完了状態。デフォルトはFalse。
    created_at: datetime - タスクの作成時刻。デフォルトは現在時刻。
    updated_at: datetime - タスクの最終更新時刻。デフォルトは現在時刻。
    """

    title: str
    description: str
    completed: bool = False
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
