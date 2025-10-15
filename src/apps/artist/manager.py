from src.dependency import db
from src.schemas import ID_Field
import sqlalchemy as sa
from sqlalchemy.exc import NoResultFound
from database.models import Author, Album, Track
from fastapi import HTTPException
from src.schemas import PaginationParams
from database.association_tables import Track_Artist


class Manager:
    def __init__(self, db: db) -> None:
        self.db = db
        self.model = Author
        self.album_model = Album
        self.track_model = Track
        self.track_artist_model = Track_Artist

    async def get_artist(self, ID: ID_Field):
        query = sa.select(self.model).where(self.model.ID == ID)
        async with self.db.get_session() as session:
            result = await session.execute(query)
        try:
            artist = result.mappings().one()
        except NoResultFound:
            raise HTTPException(404, "Artist not found.")
        return artist
    
    async def get_artist_albums(self, ID: ID_Field, pagination: PaginationParams):
        query = (sa.select(self.model, self.album_model)
                 .join(self.album_model, self.model.albums)
                 .where(self.model.ID == ID)
                 .offset(pagination.offset)
                 .limit(pagination.limit))
        async with self.db.get_session() as session:
            result = await session.execute(query)
        return result.mappings().all()
    
    async def get_artist_popular_track(self, ID: ID_Field, pagination: PaginationParams):
        """query = (sa.select(self.model, self.track_model)
                 .join(self.model, self.model.tracks)
                 .order_by(sa.desc(se)))"""
        pass