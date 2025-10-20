from pydantic import BaseModel


class CreatePlaylist(BaseModel):
    user_ID: int
    name: str | None
    is_public: bool


class Playlist(BaseModel):
    name: str | None
    is_public: bool

class Listen_History(BaseModel):
    data: list