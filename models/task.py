import enum
import uuid
from sqlalchemy import Enum, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from models.base import BaseOrm


class TaskStatus(str, enum.Enum):
    created = "СОЗДАНО"
    in_progress = "В РАБОТЕ"
    completed = "ЗАВЕРШЕНО"


class TaskOrm(BaseOrm):
    __tablename__ = "tasks"

    id: Mapped[uuid.UUID] = mapped_column(
    UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[TaskStatus] = mapped_column(
    Enum(TaskStatus, name="task_status"), nullable=False, default=TaskStatus.created
    )