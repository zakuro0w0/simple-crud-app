from fastapi import FastAPI
import sys
from pathlib import Path

# app/をpythonモジュール検索パスに追加し、app/からの相対パスでimportできるようにする
sys.path.append(str(Path(__file__).parent))

from interface import router as tasks_router

app = FastAPI()

app.include_router(tasks_router, prefix="/tasks")
