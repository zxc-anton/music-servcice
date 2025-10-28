import asyncio
from fastapi.concurrency import asynccontextmanager
import pytest
import pytest_asyncio
import httpx
from httpx import ASGITransport
from main import app
from core.db.db_dependency.connect_db import DB_dependency
from database.models import Base
from database.models import Track

@pytest.fixture(scope="session")
async def event_loop():
    event_loop = asyncio.get_event_loop()
    yield event_loop
    event_loop.close()

db_dep = DB_dependency(db_url="sqlite+aiosqlite:///")

def db_test():
    return db_dep

@pytest_asyncio.fixture
async def db_session(db_test=db_test()):
    """Настройка сессии и таблиц базы данных"""
    async with db_test._async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield db_test
    async with db_test._async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest_asyncio.fixture(scope="session")
async def client():
    """Создание тестового клиента с настройкой БД"""
    app.dependency_overrides[DB_dependency] = db_test
    async with httpx.AsyncClient(transport=ASGITransport(app), base_url="http://") as test_client:
        yield test_client
    app.dependency_overrides.clear()

@pytest_asyncio.fixture(scope="session")
async def track():
    return Track(title="title", file_url="ffewfefw")