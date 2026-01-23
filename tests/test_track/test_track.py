import pytest
import pytest_asyncio
from database.models import Track
from httpx import AsyncClient


@pytest.mark.skip
@pytest.mark.asyncio
async def test_get_track_by_id(create_track: Track, client: AsyncClient):
    response = await client.get(f"api/tracks/{create_track.ID}")
    assert response.status_code == 200
    assert response.json() == {
        "data": {
            "ID": create_track.ID,
            "type": "Track",
            "attributes": {
                "title": create_track.title,
                "album_ID": create_track.album_ID,
                "file_url": create_track.file_url,
            },
            "relationships": None,
        }
    }