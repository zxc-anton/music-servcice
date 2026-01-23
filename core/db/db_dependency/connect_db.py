from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker
from settings.setting import settings
from contextlib import asynccontextmanager
from threading import Lock


class DB_dependency:
    _instance = None
    _lock = Lock()

    def __new__(cls, *args, **kwargs):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(DB_dependency, cls).__new__(*args, **kwargs)
        return cls

    def __init__(self, db_url: str = settings.db_settings.get_url) -> None:
        self._async_engine = create_async_engine(url=db_url, echo=settings.db_settings.db_echo)
        self._async_session_maker = async_sessionmaker(autoflush=False, bind=self._async_engine)

    @asynccontextmanager
    async def get_session(self):
        async with self._async_session_maker() as session:
            try:
                yield session
            finally:
                await session.close()