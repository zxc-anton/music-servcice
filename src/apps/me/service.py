from src.apps.me.dependency import manager
from src.schemas import ID_Field
from src.apps.me.schemas import Playlist, CreatePlaylist


class Service:
    def __init__(self, manager: manager) -> None:
        self.manager = manager

    async def add_in_favorites(self, track_ID: ID_Field, user_ID: ID_Field): 
        return await self.manager.add_in_favorites(track_ID=track_ID, user_ID=user_ID)
    
    async def create_playlist(self, user_ID: ID_Field, playlist: Playlist):
        return await self.manager.create_playlist(CreatePlaylist(user_ID=user_ID.ID, name=playlist.name, is_public=playlist.is_public))
    
    async def add_track_in_playlist(self, user_ID: ID_Field, playlist_ID: ID_Field, track_ID: ID_Field):
        return await self.manager.add_track_in_playlist(track_ID=track_ID, playlist_ID=playlist_ID, user_ID=user_ID)
    
    async def delete_track_from_favorits(self, user_ID: ID_Field, track_ID: ID_Field):
        return await self.manager.delete_track_from_favorits(user_ID=user_ID, track_ID=track_ID)
    
    async def delete_track_from_playlist(self, user_ID: ID_Field, track_ID: ID_Field, playlist_ID):
        return await self.manager.delete_track_from_playlist(user_ID=user_ID, playlist_ID=playlist_ID, track_ID=track_ID)
    
    async def delete_playlist(self, user_ID: ID_Field, playlist_ID: ID_Field):
        return await self.manager.delete_playlist(user_ID=user_ID, playlist_ID=playlist_ID)