from src.dependency import db
import sqlalchemy as sa
from src.schemas import ID_Field
from database.models import Album, Track
from sqlalchemy.exc import NoResultFound
from fastapi import HTTPException
from database.association_tables import Album_Track
from src.apps.album.schemas import (Album_Response, Album_Attributes, 
                                    Album_Schema, Album_Tracks_Response)
from src.apps.track.schemas import Track_Schema, Track_Attributes


class Manager:
    def __init__(self, db: db) -> None:
        self.db = db
        self.model = Album
        self.track_model = Track
        self.album_track_model = Album_Track

    async def get_album(self, ID: ID_Field) -> Album_Response:
        query = sa.select(self.model).where(self.model.ID == ID)
        async with self.db.get_session() as session:
            result = await session.execute(query)
        try:
            album =  result.scalar_one()
            return Album_Response(data=Album_Schema(ID=album.ID, 
                                                    attributes=Album_Attributes(title=album.title, cover_url=album.cover_url),
                                                    ))
        except  NoResultFound: 
            raise HTTPException(404, "Album not found.")
        
    async def get_album_tracks(self, ID: ID_Field):
        query =(sa.select(self.track_model)
                .where(self.track_model.album_ID==ID)
            )
        async with self.db.get_session() as session:
            result = await session.execute(query)
        tracks = result.scalars()
        return Album_Tracks_Response(data=[Track_Schema(ID=track.ID, attributes=Track_Attributes(title=track.title, album_ID=track.album_ID, file_url=track.file_url)) for track in tracks])