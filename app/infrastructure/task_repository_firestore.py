from google.cloud import firestore
from dotenv import load_dotenv, find_dotenv
import os
from domain import Task
from application import ITaskRepository

# .envファイルが存在する場合にのみそれを読み込む
load_dotenv(find_dotenv())
# 環境変数からプロジェクトIDを取得
project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
db = firestore.Client(project=project_id)


class TaskRepositoryFirestore(ITaskRepository):
    def add(self, task: Task) -> Task:
        update_time, doc_ref = db.collection("tasks").add(task.model_dump())
        task.updated_at = update_time
        return {"id": doc_ref.id, "task": task}
