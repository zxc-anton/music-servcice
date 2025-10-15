from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession, AsyncEngine
from settings.setting import settings
from contextlib import asynccontextmanager
from typing import Any


class DB_dependency:
    def __init__(self):
        self._url: str = settings.db_settings.get_url
        self._async_engine: AsyncEngine = create_async_engine(self._url, echo=settings.db_settings.db_echo, pool_size=settings.db_settings.db_pool_size)
        self._async_session_fabric = async_sessionmaker(bind=self._async_engine, expire_on_commit=False, autoflush=False)

    @asynccontextmanager
    async def get_session(self):
        async with self._async_session_fabric() as session:
            try:
                yield session
            finally:
                await session.close()
    
    async def close_db(self):
        print("зфкрыто")
        await self._async_engine.dispose()