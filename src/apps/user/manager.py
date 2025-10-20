import trace
from src.dependency import db
from src.schemas import (ID_Field, Pagination_Params, 
                        User_Response, User_Attributes, 
                        User_Schema)
from src.apps.track.schemas import Track_Schema, Track_Attributes
from src.apps.user.schemas import (Listen_History_Response, Playlists_Response, 
                                   Playlist_Attributes, Playlist_Schema,
                                   Favorits_Response)
from database.models import Track, Author, User, Playlist
import sqlalchemy as sa
from database.association_tables import Listen_History, favorites
from sqlalchemy.exc import NoResultFound
from fastapi import HTTPException




class Manager:
    def __init__(self, db: db) -> None:
        self.db = db
        self.track_model = Track
        self.author_model = Author
        self.model = User
        self.listen_history = Listen_History
        self.playlist_model = Playlist
        self.favorites = favorites


    async def get_user(self, ID: ID_Field) -> User_Response:

        query = (sa.select(self.model).where(self.model.ID == ID.ID))
        async with self.db.get_session() as session:
            result = await session.execute(query)
        try:
            user = result.scalar_one()
            return User_Response(data=User_Schema(ID=user.ID, attributes=User_Attributes(name=user.name, avatar_url=user.avatar_url)))
        except NoResultFound:
            raise HTTPException(404, "User not found.")



    async def get_listen_history(self, pagination: Pagination_Params, ID: ID_Field) -> Listen_History_Response:
        query = (sa.select(self.model.ID, self.track_model.title, self.track_model.file_url, self.track_model.album_ID, self.listen_history.c.track_ID, self.listen_history.c.listened_at, self.author_model.ID,
                           self.author_model.name, self.author_model.photo_url)
                 .join(self.model, self.model.ID == self.listen_history.c.user_ID)
                 .join(self.author_model, self.track_model.authors)
                 .where(self.model.ID == ID.ID)
                 .order_by(sa.desc(self.listen_history.c.listened_at))
                 .offset(pagination.offset)
                 .limit(pagination.limit))
        async with self.db.get_session() as session:
            result = await session.execute(query)
        return Listen_History_Response(data=[ Track_Schema(ID=track["ID"], attributes=Track_Attributes(title=track["title"], album_ID=track["album_ID"], file_url=track["file_url"])) for track in result.mappings().all()])
    
    async def get_playlists(self, ID: ID_Field, pagination: Pagination_Params) -> Playlists_Response:
        query = (sa.select(self.playlist_model).where(self.playlist_model.user_ID == ID.ID)
                 .offset(pagination.offset)
                 .limit(pagination.limit))
        async with self.db.get_session() as session:
            result = await session.execute(query)
        playlists = result.scalars()
        return Playlists_Response(data=[Playlist_Schema(ID=playlist.ID, attributes=Playlist_Attributes(name=playlist.name, cover_url=playlist.cover_url, is_public=playlist.is_public)) for playlist in playlists])
    
    async def get_favorits(self, ID: ID_Field, pagination: Pagination_Params) -> Favorits_Response:
        query = (sa.select(self.model.ID.label("user"), self.track_model.ID, self.track_model.album_ID, self.track_model.title, self.track_model.file_url)
                 .join(self.favorites, self.favorites.c.user_ID == self.model.ID)
                 .join(self.track_model, self.favorites.c.track_ID == self.track_model.ID)
                 .where(self.model.ID == ID.ID)
                 .offset(pagination.offset)
                 .limit(pagination.limit))
        async with self.db.get_session() as session:
            result = await session.execute(query)
        tracks = result.mappings().all()
        return Favorits_Response(data=[Track_Schema(ID=track["ID"], attributes=Track_Attributes(title=track["title"], album_ID=track["album_ID"], file_url=track["file_url"])) for track in tracks])