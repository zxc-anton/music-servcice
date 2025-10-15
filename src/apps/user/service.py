from src.apps.user.dependency import manager
from src.schemas import ID_Field, PaginationParams


class Service:
    def __init__(self, manager: manager) -> None:
        self.manager = manager

    async def get_user(self, ID: ID_Field):
        return await self.manager.get_user(ID=ID)

    async def get_listen_history(self, pagination: PaginationParams, ID: ID_Field):
        return await self.manager.get_listen_history(pagination=pagination, ID=ID)
    
    async def get_playlists(self, ID: ID_Field, pagination: PaginationParams):
        return await self.manager.get_playlists(ID=ID, pagination=pagination)
    
    async def get_favorits(self, ID: ID_Field, pagination: PaginationParams):
        return await self.manager.get_favorits(ID=ID, pagination=pagination)