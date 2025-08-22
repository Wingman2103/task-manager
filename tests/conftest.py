import asyncio
import pytest

from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.pool import NullPool

from main import app
from db.database import get_async_session
from models.base import BaseOrm
from config import settings


TEST_DATABASE = f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/test_db"
test_engine = create_async_engine(TEST_DATABASE, poolclass=NullPool)
TestSessionLocal = async_sessionmaker(bind=test_engine, class_=AsyncSession, expire_on_commit=False)


@pytest.fixture(scope="session", autouse=True)
async def prepare_database():
    async with test_engine.begin() as conn:
        await conn.run_sync(BaseOrm.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(BaseOrm.metadata.drop_all)


async def override_get_session():
    async with TestSessionLocal() as session:
        yield session


@pytest.fixture(scope="function")
async def client():

    app.dependency_overrides[get_async_session] = override_get_session
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()
