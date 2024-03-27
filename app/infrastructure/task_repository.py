import firebase_admin
from firebase_admin import credentials, firestore
import os
from domain import Task

# プロジェクトのrootディレクトリからservice-account-key.jsonのpathを構築する
current_dir = os.path.dirname(os.path.realpath(__file__))
cred_path = os.path.join(
    current_dir, "../../.devcontainer/gcp-service-account-key.json"
)

# 認証情報からfirestoreデータベースインスタンスを作る
cred = credentials.Certificate(cred_path)
firebase_admin.initialize_app(cred)
db = firestore.client()


class TaskRepository:
    def add(self, task: Task) -> Task:
        update_time, doc_ref = db.collection("tasks").add(task.model_dump())
        task.id = doc_ref.id
        task.updated_at = update_time
        return task
