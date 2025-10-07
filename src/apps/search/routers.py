from src.apps.search.main import router
from src.apps.search.dependency import service
from fastapi import Query


@router.get("/")
async def search(service: service, q: str = Query()):
    return await service.search(q=q)