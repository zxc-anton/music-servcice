from pydantic import BaseModel, ConfigDict, model_validator
from src.schemas import Links, ID_Field
from database.models import Album
from settings.setting import settings
from src.apps.track.schemas import Track_Schema

class Track_Links(BaseModel):
    links: Links


class Album_Relationships(BaseModel):
    tracks: Track_Links
    model_config = ConfigDict(extra="ignore")

class Album_Attributes(BaseModel):
    title: str
    cover_url: str

    model_config = ConfigDict(extra="ignore")

class Album_Schema(ID_Field, BaseModel): 
    type: str = Album.__name__
    attributes: Album_Attributes
    relationships: Album_Relationships | None = None

    @model_validator(mode="after")
    def update_relationships(self):
        if self.relationships is None:
            self.relationships = Album_Relationships(
                tracks=Track_Links(
                    links=Links(
                        self=f"{settings.backend_url}/albums/{self.ID}/tracks")
                        )
                        )
        return self
    
    model_config = ConfigDict(extra="ignore")
    
class Album_Response(BaseModel):
    data: Album_Schema
    model_config = ConfigDict(extra="ignore")



class Album_Tracks_Response(BaseModel):
    data: list[Track_Schema] = []