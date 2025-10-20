from src.apps.artist.dependency import manager
from src.schemas import ID_Field
from src.schemas import Pagination_Params
from src.apps.artist.schemas import Artist_Response, Albums_Response


class Service:
    def __init__(self, manager: manager) -> None:
        self.manager = manager

    async def get_artist(self, ID: ID_Field) -> Artist_Response:
        return await self.manager.get_artist(ID=ID)
    
    async def get_artist_albums(self, ID: ID_Field, pagination: Pagination_Params) -> Albums_Response:
        return await self.manager.get_artist_albums(ID=ID, pagination=pagination)
    
    async def get_artist_popular_track(self, ID: ID_Field, pagination: Pagination_Params):
        return await self.manager.get_artist_popular_track(ID=ID, pagination=pagination)