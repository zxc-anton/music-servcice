from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker
from settings.setting import settings
from contextlib import asynccontextmanager


class DB_dependency:
    def __init__(self) -> None:
        self._async_engine = create_async_engine(url=settings.db_settings.get_url, echo=settings.db_settings.db_echo)
        self._async_session_maker = async_sessionmaker(autoflush=False, bind=self._async_engine)

    @asynccontextmanager
    async def get_session(self):
        async with self._async_session_maker() as session:
            try:
                yield session
            finally:
                await session.close()