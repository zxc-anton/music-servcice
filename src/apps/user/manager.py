from functools import cache
from src.dependency import db
from src.schemas import ID_Field, PaginationParams
from database.models import Track, Author, User, Playlist
import sqlalchemy as sa
from database.association_tables import Listen_History, favorites
from sqlalchemy.exc import NoResultFound
from fastapi import HTTPException
from asyncpg.exceptions import ConnectionDoesNotExistError
from functools import lru_cache




class Manager:
    def __init__(self, db: db) -> None:
        self.db = db
        self.track_model = Track
        self.author_model = Author
        self.model = User
        self.listen_history = Listen_History
        self.playlist_model = Playlist
        self.favorites = favorites


    async def get_user(self, ID: ID_Field):

        query = (sa.select(self.model).where(self.model.ID == ID.ID))
        try:
            async with self.db.get_session() as session:
                result = await session.execute(query)
            try:
                return result.mappings().one()
            except NoResultFound:
                raise HTTPException(404, "User not found.")
        except ConnectionDoesNotExistError:
            raise HTTPException(408)


    async def get_listen_history(self, pagination: PaginationParams, ID: ID_Field):
        query = (sa.select(self.model.ID, self.track_model.title, self.track_model.file_url, self.listen_history.c.track_ID, self.listen_history.c.listened_at, self.author_model.ID,
                           self.author_model.name, self.author_model.photo_url)
                 .join(self.model, self.model.ID == self.listen_history.c.user_ID)
                 .join(self.author_model, self.track_model.authors)
                 .where(self.model.ID == ID.ID)
                 .order_by(sa.desc(self.listen_history.c.listened_at))
                 .offset(pagination.offset)
                 .limit(pagination.limit))
        async with self.db.get_session() as session:
            result = await session.execute(query)
        return result.mappings().all()
    
    async def get_playlists(self, ID: ID_Field, pagination: PaginationParams):
        query = (sa.select(self.playlist_model).where(self.playlist_model.user_ID == ID.ID)
                 .offset(pagination.offset)
                 .limit(pagination.limit))
        async with self.db.get_session() as session:
            result = await session.execute(query)
        return result.mappings().all()
    
    async def get_favorits(self, ID: ID_Field, pagination: PaginationParams):
        query = (sa.select(self.model, self.favorites, self.track_model)
                 .join(self.favorites, self.favorites.c.user_ID == self.model.ID)
                 .where(self.model.ID == ID.ID)
                 .join(self.track_model, self.favorites.c.track_ID == self.track_model.ID)
                 .offset(pagination.offset)
                 .limit(pagination.limit))
        async with self.db.get_session() as session:
            result = await session.execute(query)
        return result.mappings().all()