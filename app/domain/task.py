from pydantic import BaseModel, Field
from datetime import datetime


class Task(BaseModel):
    title: str
    description: str
    completed: bool = False
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
