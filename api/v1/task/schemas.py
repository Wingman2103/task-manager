from uuid import UUID
from pydantic import BaseModel, Field

from models.task import TaskStatus


class TaskCreate(BaseModel):
    title: str = Field("", min_length=1, max_length=255)
    description: str | None = None
    status: TaskStatus = TaskStatus.created


class TaskUpdate(BaseModel):
    title: str | None = Field(None, max_length=255)
    description: str | None = None
    status: TaskStatus | None = None


class TaskRead(BaseModel):
    id: UUID
    title: str
    description: str | None
    status: TaskStatus

