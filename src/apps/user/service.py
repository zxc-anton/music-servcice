from src.apps.user.dependency import manager
from src.apps.auth.schemas import UserResponse
from src.apps.track.schemas import Pagination


class Service:
    def __init__(self, manager: manager) -> None:
        self.manager = manager


    async def get_listen_history(self, params: Pagination, user: UserResponse):
        return await self.manager.get_listen_history(params=params, ID=user.ID)