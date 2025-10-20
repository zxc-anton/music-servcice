from pydantic import BaseModel, ConfigDict
from src.schemas import ID_Field
from database.models import Track

class _track(ID_Field, BaseModel):
    title: str
    album_ID: int | None 
    file_url: str
    model_config = ConfigDict(extra="ignore")

class Popular_Tracks_Schema(BaseModel):
    favorits: list[_track]
    listen_count: int
    model_config = ConfigDict(extra="ignore")

class Track_Attributes(BaseModel): 
    title: str 
    album_ID: int | None
    file_url: str
    model_config = ConfigDict(extra="ignore")

class Track_Relationships(BaseModel): pass

class Track_Schema(ID_Field, BaseModel):
    type: str = Track.__name__
    attributes: Track_Attributes
    relationships: Track_Relationships | None = None