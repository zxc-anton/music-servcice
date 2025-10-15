from src.apps.album.depenency import manager
from src.schemas import ID_Field

class Service: 
    def __init__(self, manager: manager) -> None:
        self.manager = manager

    async def get_album(self, ID: ID_Field):
        return await self.manager.get_album(ID=ID)
    
    async def get_album_tracks(self, ID: ID_Field):
        return await self.manager.get_album_track(ID=ID)