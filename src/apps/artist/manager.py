from src.dependency import db
from src.schemas import ID_Field
import sqlalchemy as sa
from sqlalchemy.exc import NoResultFound
from database.models import Author, Album, Track
from fastapi import HTTPException
from src.schemas import Pagination_Params
from database.association_tables import Track_Artist, Album_Author
from src.apps.artist.schemas import (Artist_Response, Artist_Schema, 
                                     Artist_Attributes, Albums_Response, 
                                     )
from sqlalchemy import func
from src.apps.album.schemas import Album_Schema, Album_Attributes, Album_Relationships
class Manager:
    def __init__(self, db: db) -> None:
        self.db = db
        self.model = Author
        self.album_model = Album
        self.track_model = Track
        self.track_artist_model = Track_Artist
        self.album_author_model = Album_Author

    async def get_artist(self, ID: ID_Field) -> Artist_Response:
        query = sa.select(self.model.ID, self.model.name, self.model.photo_url).where(self.model.ID == ID)
        async with self.db.get_session() as session:
            result = await session.execute(query)
        try:
            artist = result.mappings().one()
        except NoResultFound:
            raise HTTPException(404, "Artist not found.")
        return Artist_Response(data=Artist_Schema(attributes=Artist_Attributes(**artist), ID=artist["ID"]))
    
    async def get_artist_albums(self, ID: ID_Field, pagination: Pagination_Params) -> Albums_Response:
        query = (sa.select(self.model.ID.label("author_id"), self.album_model.ID, self.album_model.title, self.album_model.cover_url)
                 .join(self.album_author_model, self.model.ID == self.album_author_model.c.author_ID)
                 .join(self.album_model, self.album_model.ID == self.album_author_model.c.album_ID)
                 .where(self.model.ID == ID)
                 .offset(pagination.offset)
                 .limit(pagination.limit))
        async with self.db.get_session() as session:
            result = await session.execute(query)
        return Albums_Response(data=[Album_Schema(ID=album["ID"], attributes=Album_Attributes(**album)) for album in result.mappings().all()])
    
    async def get_artist_popular_track(self, ID: ID_Field, pagination: Pagination_Params):
        """query = (sa.select(self.model, self.track_model)
                 .join(self.model, self.model.tracks)
                 .order_by(sa.desc(se)))"""
        query = (
            sa.select(self.model, self.track_model, self.track_artist_model, func.count(self.track_model.listening_users))
            .join(self.model, self.track_artist_model.c.author_ID == self.model.ID)
            .join(self.track_model, self.track_model.ID == self.track_artist_model.c.track_ID)
            .group_by(self.model, self.track_model, self.track_artist_model)
            
        )
        async with self.db.get_session() as session:
            result = await session.execute(query)
            tracks = result.mappings().all()
        return tracks