from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.task.schemas import TaskCreate, TaskUpdate
from models.task import TaskOrm


class TaskCRUD:

    async def get(self, id: UUID, session: AsyncSession) -> TaskOrm | None:
        query = (select(TaskOrm).where(TaskOrm.id == id))
        result = await session.execute(query)
        return result.unique().scalars().first()
    
    async def get_by_title(self, title: str, session: AsyncSession) -> list[TaskOrm] | None:
        query = (select(TaskOrm).where(TaskOrm.title == title).order_by(TaskOrm.title))
        result = await session.execute(query)
        return result.unique().scalars().all()
    
    async def get_list(self, session: AsyncSession) -> list[TaskOrm] | None:
        query = (select(TaskOrm).order_by(TaskOrm.id))
        result = await session.execute(query)
        return result.unique().scalars().all()
    
    async def create(self, task_body: TaskCreate, session: AsyncSession) -> int | None:
        try:
            task = TaskOrm(**task_body.model_dump())
            session.add(task)
            await session.commit()
            return task.id
        except Exception:
            await session.rollback()
            raise

    async def update(self, task: TaskOrm, task_body: TaskUpdate, session: AsyncSession) -> TaskOrm | None:
        try:
            for attr, value in task_body.model_dump().items():
                if value == None:
                    continue
                setattr(task, attr, value)

            await session.commit()
            await session.refresh(task)
            
            return task
        except Exception:
            await session.rollback()
            raise
    
    async def delete(self, task: TaskOrm, session: AsyncSession) -> bool | None:
        try:
            await session.delete(task)
            await session.commit()
            return True
        except Exception:
            await session.rollback()
            raise