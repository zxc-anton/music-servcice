from pydantic import BaseModel
from src.apps.track.schemas import Track_Schema
from database.models import Playlist
from src.schemas import ID_Field, Name_Field


class Listen_History_Response(BaseModel):
    data: list[Track_Schema] = []

class Playlist_Relationships(BaseModel): pass


class Playlist_Attributes(Name_Field, BaseModel):
    cover_url: str | None 
    is_public: bool

class Playlist_Schema(ID_Field, BaseModel): 
    type: str = Playlist.__name__
    attributes: Playlist_Attributes
    relationships: Playlist_Relationships | None = None

class Playlists_Response(BaseModel): 
    data: list[Playlist_Schema] = []

class Favorits_Response(BaseModel):
    data: list[Track_Schema] = []