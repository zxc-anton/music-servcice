from pydantic import BaseModel
from src.schemas import ID_Field


class CreatePlaylist(BaseModel):
    user_ID: ID_Field
    name: str | None
    is_public: bool


class Playlist(BaseModel):
    name: str | None
    is_public: bool