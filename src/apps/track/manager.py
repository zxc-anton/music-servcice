from src.dependency import db
from database.models import Track, User, Author
from src.schemas import ID_Field, Pagination_Params
import sqlalchemy as sa
from database.association_tables import Track_Artist
from sqlalchemy import func
from sqlalchemy.exc import NoResultFound
from fastapi import HTTPException
from src.apps.track.schemas import Track_Attributes, Popular_Tracks_Schema, Track_Response, Track_Schema, Popular_Tracks_Response, Popular_Track_Attributes


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
            result = await session.get(self.model, ID.ID)
            try:
                return result
            
                #return Track_Response(data=Track_Schema(ID=track["ID"], attributes=Track_Attributes(title=track["title"], file_url=track["file_url"], album_ID=track["album_ID"])))
            except NoResultFound:
                raise HTTPException(404, "Track not found.")

        
    async def get_popular_tracks(self, params: Pagination_Params) :
        query = (
            sa.select(
                self.model.ID, self.model.title, self.model.album_ID, self.model.file_url,
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
        return Popular_Tracks_Response(data=[Popular_Tracks_Schema(ID=track["ID"], attributes=Popular_Track_Attributes(title=track["title"], album_ID=track["album_ID"], file_url=track["file_url"], listen_count=track["listen_count"])) for track in tracks])
     
    

