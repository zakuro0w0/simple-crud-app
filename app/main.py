from fastapi import FastAPI
from .interface.routes import router as tasks_router

app = FastAPI()

app.include_router(tasks_router, prefix="/tasks")
