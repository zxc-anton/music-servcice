from urllib import response
import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
@pytest.mark.parametrize("query", ["title", "ti", "it"])
async def test_search_track(client: AsyncClient, query: str):
    response = await client.get(f"api/search?q={query}")
    assert response.status_code == 200
    print(response.json())
    assert response.json() != {}