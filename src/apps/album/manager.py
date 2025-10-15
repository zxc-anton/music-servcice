from src.dependency import db
import sqlalchemy as sa
from src.schemas import ID_Field
from database.models import Album, Track
from sqlalchemy.exc import NoResultFound
from fastapi import HTTPException
from database.association_tables import Album_Track


class Manager:
    def __init__(self, db: db) -> None:
        self.db = db
        self.model = Album
        self.track_model = Track
        self.album_track_model = Album_Track

    async def get_album(self, ID: ID_Field):
        query = sa.select(self.model).where(self.model.ID == ID)
        async with self.db.get_session() as session:
            result = await session.execute(query)
        try:
            return result.mappings().one()
        except  NoResultFound: 
            raise HTTPException(404, "Album not found.")
        
    async def get_album_track(self, ID: ID_Field):
        query =(sa.select(self.model, self.track_model)
                .where(self.model.ID==ID)
                .join(self.album_track_model, self.album_track_model.c.album_ID==self.model.ID)
                .join(self.track_model, self.album_track_model.c.track_ID==self.track_model.ID))
        async with self.db.get_session() as session:
            result = await session.execute(query)
        return result.mappings().all()