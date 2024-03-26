import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# ## file description
# - firestoreにデータを挿入する

# Firebase Admin SDKの初期化
# サービスアカウントのキーファイルを参照して認証する
cred = credentials.Certificate("../.devcontainer/gcp-service-account-key.json")
# 認証情報からFirebaseアプリケーションインスタンスを作成
app = firebase_admin.initialize_app(cred)
# Firestoreのインスタンスを取得
# - Firestoreのデータベース名は指定できない
# - GCPプロジェクトIDに紐付く"(default)"という名前のデータベースを参照する
# - このため、Terraformで作るFirestoreリソースのnameは"(default)"にする必要がある
db = firestore.client(app)

# ToDoリストのデータ
todos = [
    {"title": "買い物に行く", "completed": False},
    {"title": "犬の散歩", "completed": True},
    # その他のタスク...
]

# ToDoリストのデータをFirestoreに挿入
for todo in todos:
    doc_ref = db.collection("todos").document()  # 新しいドキュメントIDを自動生成
    doc_ref.set(
        {
            "title": todo["title"],
            "completed": todo["completed"],
            "createdAt": firestore.SERVER_TIMESTAMP,  # サーバーのタイムスタンプを使用
        }
    )
