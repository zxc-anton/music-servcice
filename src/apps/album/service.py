from src.apps.album.depenency import manager
from src.schemas import ID_Field
from src.apps.album.schemas import Album_Response, Album_Tracks_Response

class Service: 
    def __init__(self, manager: manager) -> None:
        self.manager = manager

    async def get_album(self, ID: ID_Field) -> Album_Response:
        return await self.manager.get_album(ID=ID)
    
    async def get_album_tracks(self, ID: ID_Field) -> Album_Tracks_Response:
        return await self.manager.get_album_tracks(ID=ID)