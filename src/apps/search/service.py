from src.apps.search.dependency import manager



class Service:
    def __init__(self, manager: manager) -> None:
        self.manager = manager

    async def search(self, q: str):
        return await self.manager.search(q=f"%{q}%")