from src.apps.artist.dependency import manager
from src.schemas import ID_Field
from src.schemas import PaginationParams


class Service:
    def __init__(self, manager: manager) -> None:
        self.manager = manager

    async def get_artist(self, ID: ID_Field):
        return await self.manager.get_artist(ID=ID)
    
    async def get_artist_albums(self, ID: ID_Field, pagination: PaginationParams):
        return await self.manager.get_artist_albums(ID=ID, pagination=pagination)