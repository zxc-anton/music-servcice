from src.apps.playlist.schemas import Playlist_Tracks_Response
from src.dependency import db
from src.schemas import ID_Field
import sqlalchemy as sa
from database.models import Playlist, Track
from database.association_tables import Playlist_Track
from src.apps.track.schemas import Track_Schema, Track_Attributes

class Manager:
    def __init__(self, db: db) -> None:
        self.db = db
        self.model = Playlist
        self.track_model = Track
        self.playlist_track_model = Playlist_Track

    async def get_playlist_tracks(self, ID: ID_Field):
        query = (sa.select(self.model.ID.label("playlist_ID") , self.track_model.title, self.track_model.album_ID, self.track_model.file_url, self.track_model.ID)
                 .join(self.playlist_track_model, self.model.ID == self.playlist_track_model.c.playlist_ID)
                 .join(self.track_model, self.playlist_track_model.c.track_ID==self.track_model.ID)
                 .where(self.model.ID == ID))
        async with self.db.get_session() as session:
            result = await session.execute(query)
        tracks = result.mappings().all()
        return Playlist_Tracks_Response(data=[Track_Schema(ID=track["ID"], attributes=Track_Attributes(title=track["title"], album_ID=track["album_ID"], file_url=track["file_url"])) for track in tracks])