import http
import httpx
import pytest
import pytest_asyncio
from httpx import AsyncClient

from core.db.db_dependency.connect_db import DB_dependency
from database.models import Playlist, Track
import sqlalchemy as sa
from database.association_tables import Playlist_Track


@pytest_asyncio.fixture(scope="session")
async def add_tracks_in_playlist(db_session: DB_dependency,
                                 create_track: Track,
                                 create_user_playlists: Playlist):
    async with db_session.get_session() as session:
        query = sa.insert(Playlist_Track).values(playlist_ID=create_user_playlists.ID, track_ID=create_track.ID)
        await session.execute(query)
        yield create_user_playlists, create_track



@pytest.mark.asyncio
async def test_get_track_from_playlist(add_tracks_in_playlist: tuple[Playlist, Track], client: AsyncClient):
    playlist, track = add_tracks_in_playlist
    response = await client.get(f"api/playlists/{playlist.ID}/tracks")
    assert response.status_code == 200
    assert response.json() == {
        "data": [
            {
            "type": "Track",
            "ID": track.ID, 
            "attributes": {
                "title": track.title,
                "album_ID": track.album_ID,
                "file_url": track.file_url,
            },
            "relationships": None
            }
        ]
    }