from src.apps.track.depends import manager
from src.schemas import ID_Field, PaginationParams
from src.apps.track.schemas import Track_Schema, Popular_Tracks_Schema


class Service:
    def __init__(self, manager: manager) -> None:
        self.manager = manager


    async def get_track_by_id(self, ID: ID_Field):
        return await self.manager.get_track_by_id(ID=ID)
    
    async def get_popular_tracks(self, params: PaginationParams):
        return await self.manager.get_popular_tracks(params=params)
    

    