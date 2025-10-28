from pydantic import BaseModel, ConfigDict
from src.schemas import ID_Field
from database.models import Track


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

class Track_Response(BaseModel):
    data: Track_Schema

class Popular_Track_Attributes(Track_Attributes, BaseModel):
    listen_count: int

class Popular_Tracks_Schema(ID_Field, BaseModel):
    type: str = Track.__name__
    attributes: Popular_Track_Attributes
    relationships: None = None
    model_config = ConfigDict(extra="ignore")

class Popular_Tracks_Response(BaseModel):
    data: list[Popular_Tracks_Schema] = []