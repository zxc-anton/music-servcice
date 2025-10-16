from src.dependency import db
from database.models import Track, User, Author
from src.schemas import ID_Field, PaginationParams
import sqlalchemy as sa
from database.association_tables import Track_Artist
from sqlalchemy import func
from sqlalchemy.exc import NoResultFound
from fastapi import HTTPException
from src.apps.track.schemas import Track_Schema, Popular_Tracks_Schema


class Manager:
    def __init__(self, db: db) -> None:
        self.model = Track
        self.author_model = Author
        self.user_model = User
        self.track_artist = Track_Artist
        self.db = db

    async def get_track_by_id(self, ID: ID_Field):
        query = (sa.select(self.model)
                           .where(self.model.ID==ID.ID))
        async with self.db.get_session() as session:
            result = await session.execute(query) 
        try:
            print(result.mappings().one())
        except NoResultFound:
            raise HTTPException(404, "Track not found.")

        
    async def get_popular_tracks(self, params: PaginationParams) :
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
            tracks = result.mappings().all()
        return Popular_Tracks_Schema(favorits=[Track_Schema(**track) for track in tracks], listen_count=tracks)
    
    

