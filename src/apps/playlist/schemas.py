from pydantic import BaseModel
from src.apps.track.schemas import Track_Schema


class Playlist_Tracks_Response(BaseModel):
    data: list[Track_Schema] = []