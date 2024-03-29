from pydantic import BaseModel, Field
from datetime import datetime
from zoneinfo import ZoneInfo


class Task(BaseModel):
    """
    タスクモデル。

    属性:
    title: str - タスクのタイトル。
    description: str - タスクの説明。
    completed: bool - タスクの完了状態。デフォルトはFalse。
    created_at: datetime - タスクの作成時刻(JST)。デフォルトは現在時刻。
    updated_at: datetime - タスクの最終更新時刻(JST)。デフォルトは現在時刻。
    """

    title: str
    description: str
    completed: bool = False
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(ZoneInfo("Asia/Tokyo"))
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(ZoneInfo("Asia/Tokyo"))
    )
