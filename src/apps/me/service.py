from src.apps.me.dependency import manager
from src.schemas import ID_Field
from src.apps.me.schemas import Playlist, CreatePlaylist


class Service:
    def __init__(self, manager: manager) -> None:
        self.manager = manager

    async def add_in_favorites(self, track_ID: ID_Field, user_ID: ID_Field): 
        return await self.manager.add_in_favorites(track_ID=track_ID, user_ID=user_ID)
    
    async def create_playlist(self, user_ID: ID_Field, playlist: Playlist):
        return await self.manager.create_playlist(CreatePlaylist(user_ID=user_ID, name=playlist.name, is_public=playlist.is_public))