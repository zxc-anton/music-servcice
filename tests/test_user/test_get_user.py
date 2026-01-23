from re import A
import pytest
import pytest_asyncio
from httpx import AsyncClient
from core.db.db_dependency.connect_db import DB_dependency
from database.models import Playlist, Track, User, favorites
from database.association_tables import Listen_History
import sqlalchemy as sa

        

@pytest_asyncio.fixture(scope="session")
async def create_user_listen_history(create_user: User, db_session: DB_dependency, create_track: Track):
    async with db_session.get_session() as session:
        query = sa.insert(Listen_History).values(user_ID=create_user.ID, track_ID=create_track.ID, listening_time=100)
        await session.execute(query)
        await session.commit()
        print("create liste_h")
        yield create_user, create_track
        print("exit listrn_h")



@pytest_asyncio.fixture(scope="session")
async def create_user_favorits(create_user: User, db_session: DB_dependency, create_track: Track):
    async with db_session.get_session() as session:
        query = (sa.insert(favorites).values(user_ID=create_user.ID, track_ID=create_track.ID))
        await session.execute(query)
        await session.commit()
        yield create_track, create_user



@pytest.mark.asyncio
async def test_get_user(client: AsyncClient, create_user: User):
    response = await client.get(f"api/users/{create_user.ID}")
    assert response.status_code == 200
    print(response.json())
    assert response.json() == {
        "data": {
            "type": "User",
            "ID": create_user.ID,
            "attributes": {
                "name": create_user.name,
                "avatar_url": create_user.avatar_url
            },
            "relationships": None
        }
    }

@pytest.mark.skip
@pytest.mark.asyncio
async def test_get_user_listen_history(client: AsyncClient,  create_user_listen_history: tuple[User, Track]):
    user, track = create_user_listen_history
    response = await client.get(f"api/users/{user.ID}/listen_history")
    assert response.status_code == 200
    assert response.json() == {
        "data": [
            {
                "type": "Track",
                "ID": track.ID,
                "attributes": {
                    "title": track.title,
                    "album_ID": track.album_ID,
                    "file_url": track.file_url
                },
                "relationships": None
            }
        ]
    }


@pytest.mark.asyncio
async def test_get_user_favorits(client: AsyncClient, create_user: User, create_user_favorits: tuple[Track, User]):
    response = await client.get(f"api/users/{create_user.ID}/favorits")
    track, _ = create_user_favorits
    assert response.status_code == 200
    assert response.json() == {
        "data": [
            {
                "type": "Track",
                "ID": track.ID,
                "attributes": {
                    "title": track.title,
                    "album_ID": track.album_ID,
                    "file_url": track.file_url
                },
                "relationships": None
            }
        ]
    }


@pytest.mark.asyncio
async def test_get_user_playlists(client: AsyncClient, create_user: User, create_user_playlists: Playlist):
    response = await client.get(f"api/users/{create_user.ID}/playlists")
    playlist = create_user_playlists
    assert response.status_code == 200
    assert response.json() == {
        "data": [
            {
                "type": "Playlist",
                "ID": playlist.ID,
                "attributes": {
                    "cover_url": playlist.cover_url,
                    "is_public": playlist.is_public,
                    "name": playlist.name
                },
                "relationships": None
            }

        ]
    }
    