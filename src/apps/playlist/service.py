from src.apps.playlist.dependecy import manager


class Service:
    def __init__(self, manager: manager) -> None:
        self.manager = manager

    async def get_playlist_tracks(self, ID):
        return await self.manager.get_playlist_tracks(ID=ID)