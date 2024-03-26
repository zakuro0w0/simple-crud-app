from fastapi import FastAPI
from pydantic import BaseModel
from typing import Union, Optional
import firebase_admin
from firebase_admin import credentials, firestore
import os

app = FastAPI()

# プロジェクトのrootディレクトリからservice-account-key.jsonのpathを構築する
current_dir = os.path.dirname(os.path.realpath(__file__))
cred_path = os.path.join(current_dir, "../.devcontainer/gcp-service-account-key.json")

# 認証情報からfirestoreデータベースインスタンスを作る
cred = credentials.Certificate(cred_path)
firebase_admin.initialize_app(cred)
db = firestore.client()


class Task(BaseModel):
    title: str
    description: str
    completed: Optional[bool] = False


@app.post("/tasks/")
async def create_task(task: Task):
    doc_ref = db.collection("tasks").add(task.model_dump())
    return {"id": doc_ref[1].id, "task": task}
