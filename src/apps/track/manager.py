from curses.ascii import US
from src.apps.track.depends import db
from database.models import Track, User, Author
from src.apps.track.schemas import ID_Field, Pagination
import sqlalchemy as sa
from database.association_tables import Track_Artist
from sqlalchemy import func


class Manager:
    def __init__(self, db: db) -> None:
        self.model = Track
        self.author_model = Author
        self.user_model = User
        self.track_artist = Track_Artist
        self.db = db

    async def get_track_by_id(self, ID: ID_Field):
        query = (sa.select(self.model.ID, self.model.file_url, self.author_model.ID, 
                           self.author_model.name, self.author_model.photo_url)
                           .join(self.author_model, self.model.authors)).where(self.model.ID==ID)
        async with self.db.get_session() as session:
            result = await session.execute(query)
        track = result.mappings().all()
        return track

        
    async def get_popular_tracks(self, params: Pagination):
        query = (
            sa.select(
                self.model,
                func.count(self.model.listening_users).label('listen_count')
            )
            .outerjoin(self.model.listening_users)  # Используем outerjoin чтобы включить треки без прослушиваний
            .group_by(self.model.ID)  # или self.model.id в зависимости от названия первичного ключа
            .order_by(func.count(self.model.listening_users).desc())
            .limit(params.limit)
            .offset(params.offset)
        )
        async with self.db.get_session() as session:
            result = await session.execute(query)
        return result.mappings().all()
    
    async def get_listen_history(self, params: Pagination, ID: ID_Field):
        query = (sa.select(self.model.ID, self.model.file_url, self.author_model.ID, 
                           self.author_model.name, self.author_model.photo_url)
                           .join(self.author_model, self.model.authors)
                           .join(self.user_model, self.user_model.listening_songs))
        async with self.db.get_session() as session:
            result = await session.execute(query)
            return result.mappings().all()

