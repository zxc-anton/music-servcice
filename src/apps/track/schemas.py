from pydantic import BaseModel, ConfigDict
from src.schemas import ID_Field


class Track_Schema(ID_Field, BaseModel):
    title: str
    album_ID: int | None 
    file_url: str
    model_config = ConfigDict(extra="ignore")

class Popular_Tracks_Schema(BaseModel):
    favorits: list[Track_Schema]
    listen_count: int
    model_config = ConfigDict(extra="ignore")