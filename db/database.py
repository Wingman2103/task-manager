from typing import Annotated, AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from config import settings
from models.base import BaseOrm
from models.task import TaskOrm


async_engine = create_async_engine(settings.DATABASE_URI)
async_session_maker = async_sessionmaker(bind=async_engine, class_=AsyncSession, expire_on_commit=False)

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session

session_depend = Annotated[AsyncSession, Depends(get_async_session)]

async def init_db() -> None:
    async with async_engine.begin() as conn:
        await conn.run_sync(BaseOrm.metadata.create_all)