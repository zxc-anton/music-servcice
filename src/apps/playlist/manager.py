from unittest import result
from src.dependency import db
from src.schemas import ID_Field
import sqlalchemy as sa
from database.models import Playlist, Track
from database.association_tables import Playlist_Track

class Manager:
    def __init__(self, db: db) -> None:
        self.db = db
        self.model = Playlist
        self.track_model = Track
        self.playlist_track_model = Playlist_Track

    async def get_playlist_tracks(self, ID: ID_Field):
        query = (sa.select(self.model, self.track_model)
                 .join(self.playlist_track_model, self.model.ID == self.playlist_track_model.c.playlist_ID)
                 .join(self.track_model, self.playlist_track_model.c.track_ID==self.track_model.ID)
                 .where(self.model.ID == ID))
        async with self.db.get_session() as session:
            result = await session.execute(query)
        return result.mappings().all()