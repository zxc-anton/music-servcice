from src.dependency import db
from src.schemas import ID_Field
import sqlalchemy as sa
from database.models import User, Playlist
from database.association_tables import favorites
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from src.apps.me.schemas import CreatePlaylist


class Manager: 
    def __init__(self, db: db) -> None:
        self.db = db
        self.model = User
        self.playlist_model = Playlist
        self.favorites = favorites

    async def add_in_favorites(self, track_ID: ID_Field, user_ID: ID_Field) -> None:
        query = sa.insert(self.favorites).values(user_ID=user_ID, track_ID=track_ID.ID)
        async with self.db.get_session() as session:
            transaction = await session.begin()
            try:
                await session.execute(query)
            except IntegrityError:
                await transaction.rollback()
                raise HTTPException(404, "Track not found.")
            await transaction.commit()
        return 
    
    async def create_playlist(self, playlist: CreatePlaylist) -> None:
        query = sa.insert(self.playlist_model).values(**playlist.model_dump())
        async with self.db.get_session() as session:
            transaction = await session.begin()
            await session.execute(query)
            await transaction.commit()
        return 

