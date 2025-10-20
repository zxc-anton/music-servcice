from src.apps.album.schemas import Album_Schema
from pydantic import BaseModel, ConfigDict, model_validator
from src.schemas import Name_Field, ID_Field, Links
from database.models import Author, Album
from settings.setting import settings


class Artist_Attributes(Name_Field, BaseModel):
    photo_url: str
    model_config = ConfigDict(extra="ignore")



class Album_Links(BaseModel):
    links: Links

class Popular_Track_Links(BaseModel):
    links: Links

class Artist_Relationships(BaseModel): 
    albums: Album_Links
    popular_track: Popular_Track_Links

def create_atrist_relationships(ID: str):
    return Artist_Relationships(albums=Album_Links(
        links=Links(self=f"{settings.backend_url}/artists/{ID}/albums")
    ),
    popular_track=Popular_Track_Links(links=Links(self=f"{settings.backend_url}/artists/{ID}/popular_tracks")))

class Artist_Schema(ID_Field, BaseModel):
    type: str =  Author.__name__
    attributes: Artist_Attributes
    relationships: Artist_Relationships | None = None
    

    model_config = ConfigDict(extra="ignore")

    @model_validator(mode='after')
    def update_relationships_id(self):
        """Обновляет ID в relationships после валидации"""
        if self.relationships is None:
            self.relationships = Artist_Relationships(albums=Album_Links(
            links=Links(self=f"{settings.backend_url}/artists/{self.ID}/albums")
            ),
            popular_track=Popular_Track_Links(links=Links(self=f"{settings.backend_url}/artists/{self.ID}/albums"))) 
        return self

    

class Artist_Response(BaseModel):
    data: Artist_Schema
    model_config = ConfigDict(extra="ignore")


class Albums_Response(BaseModel):
    data: list[Album_Schema] = []
