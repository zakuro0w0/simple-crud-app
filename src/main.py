from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Optional
import firebase_admin
from firebase_admin import credentials, firestore
import os
from datetime import datetime

app = FastAPI()

# プロジェクトのrootディレクトリからservice-account-key.jsonのpathを構築する
current_dir = os.path.dirname(os.path.realpath(__file__))
cred_path = os.path.join(current_dir, "../.devcontainer/gcp-service-account-key.json")

# 認証情報からfirestoreデータベースインスタンスを作る
cred = credentials.Certificate(cred_path)
firebase_admin.initialize_app(cred)
db = firestore.client()


class TaskIn(BaseModel):
    """
    タスクの入力モデルを表します。

    属性:
        title (str): タスクのタイトルです。
        description (str): タスクの説明です。
        completed (bool, optional): タスクが完了しているかどうかを示します。デフォルトはFalseです。
    """

    title: str
    description: str
    completed: Optional[bool] = False


class TaskOut(TaskIn):
    """
    タスクの出力モデルを表します。

    TaskInクラスを継承し、createdAtフィールドを追加します。
    """

    createdAt: datetime = Field(default_factory=datetime.now)


@app.post("/tasks/")
async def create_task(task: TaskIn):
    """
    データベースに新しいタスクを作成します。

    Args:
        task (TaskIn): 作成するタスク。

    Returns:
        dict: 作成されたタスクのIDとタスク自体を含む辞書。
    """
    task_out = TaskOut(**task.model_dump())
    doc_ref = db.collection("tasks").add(task_out.model_dump())
    return {"id": doc_ref[1].id, "task": task_out}
