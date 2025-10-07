import asyncio
import httpx
import pytest

from settings.setting import Settings
from src.main import app

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


