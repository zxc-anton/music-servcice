from src.dependency import db
from src.schemas import ID_Field
import sqlalchemy as sa
from database.models import User, Playlist
from database.association_tables import favorites, Playlist_Track
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from src.apps.me.schemas import CreatePlaylist


class Manager: 
    def __init__(self, db: db) -> None:
        self.db = db
        self.model = User
        self.playlist_model = Playlist
        self.favorites = favorites
        self.playlist_track_model = Playlist_Track

    async def add_in_favorites(self, track_ID: ID_Field, user_ID: ID_Field) -> None:
        query = sa.insert(self.favorites).values(user_ID=user_ID.ID, track_ID=track_ID.ID)
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
    
    async def add_track_in_playlist(self, track_ID, playlist_ID, user_ID):
        playlist = sa.select(self.playlist_model).where(self.playlist_model.ID == playlist_ID)
        async with self.db.get_session() as session:
            result = await session.execute(playlist)
            playlist= result.scalar()
            if playlist.user_ID != user_ID:
                raise HTTPException(403, "No user playlist")
            query = sa.insert(self.playlist_track_model).values(playlist_ID=playlist.ID, track_ID=track_ID)
            await session.execute(query)
            await session.commit()

