
from os import name
import pytest
import pytest_asyncio
from httpx import AsyncClient
from core.db.db_dependency.connect_db import DB_dependency
from database.models import Track, User
from database.association_tables import Listen_History
import sqlalchemy as sa


@pytest_asyncio.fixture(scope="function")
async def create_user(db_session: DB_dependency):
    async with db_session.get_session() as session:
        user = User(name="effew", email="fwef", password_hash="ewf")
        session.add(user)
        await session.commit()
        await session.refresh(user)
        yield user

@pytest_asyncio.fixture(scope="function")
async def create_track(db_session: DB_dependency, track: Track):
    async with db_session.get_session() as session:
        session.add(track)
        await session.commit()
        await session.refresh(track)
        yield track
        

@pytest_asyncio.fixture(scope="function")
async def create_user_listen_history(create_user: User, db_session: DB_dependency, create_track: Track):
    async with db_session.get_session() as session:
        query = sa.insert(Listen_History).values(user_ID=create_user.ID, track_ID=create_track.ID, listening_time=100)
        await session.execute(query)
        await session.commit()
        print("create liste_h")
        yield create_user, create_track
        print("exit listrn_h")


@pytest.mark.asyncio
async def test_get_user(client: AsyncClient, create_user: User):
    response = await client.get(f"api/users/{create_user.ID}")
    assert response.status_code == 200
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

@pytest.mark.asyncio
async def test_get_user_listen_history(client: AsyncClient,  create_user_listen_history: tuple[User, Track]):
    user, track = create_user_listen_history
    print(track.ID)
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
async def test_get_user_favorits(client: AsyncClient, create_user: User):
    response = await client.get(f"api/users/{create_user.ID}/listen_history")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_user_playlists(client: AsyncClient, create_user: User):
    response = await client.get(f"api/users/{create_user.ID}/playlists")
    assert response.status_code == 200
    
    