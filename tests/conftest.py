import asyncio
from fastapi.concurrency import asynccontextmanager
import pytest
import pytest_asyncio
import httpx
from httpx import ASGITransport
from main import app
from core.db.db_dependency.connect_db import DB_dependency
from database.models import Base, Track, Playlist, User

@pytest.fixture(scope="session")
async def event_loop():
    event_loop = asyncio.get_event_loop()
    yield event_loop
    event_loop.close()

db_dep = DB_dependency(db_url="sqlite+aiosqlite:///")

def db_test():
    return db_dep

@pytest_asyncio.fixture(scope="session")
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

@pytest_asyncio.fixture(scope="session")
async def create_user_playlists(create_user: User, db_session: DB_dependency):
    async with db_session.get_session() as session:
        playlist = Playlist(name="test", user_ID=create_user.ID)
        session.add(playlist)
        await session.commit()
        await session.refresh(playlist)
        yield playlist

@pytest_asyncio.fixture(scope="session")
async def create_track(db_session: DB_dependency):
    async with db_session.get_session() as session:
        track = Track(title="title", file_url="ffewfefw")
        session.add(track)
        await session.commit()
        await session.refresh(track)
        yield track


@pytest_asyncio.fixture(scope="session")
async def create_user(db_session: DB_dependency):
    async with db_session.get_session() as session:
        user = User(name="effew", email="fwef", password_hash="ewf")
        session.add(user)
        await session.commit()
        await session.refresh(user)
        yield user

@pytest_asyncio.fixture(scope="session")
async def create_album(db_session: DB_dependency):
    async with db_session.get_session() as session:
        pass
