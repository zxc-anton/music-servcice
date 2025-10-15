from src.apps.user.main import router
from src.apps.user.dependency import service
from src.dependency import pagination


@router.get("/{ID}")
async def get_user(ID: int, service: service):
    return await service.get_user(ID=ID)


@router.get("/{ID}/listen_history")
async def get_listen_history(service: service, ID: int, pagination: pagination):
    return await service.get_listen_history(pagination=pagination, ID=ID)

@router.get("/{ID}/playlists")
async def get_playlists(service: service, ID: int, pagination: pagination):
    return await service.get_playlists(ID=ID, pagination=pagination)

@router.get("/{ID}/favorits")
async def get_favorits(service: service, ID: int, pagination: pagination):
    return await service.get_favorits(ID=ID, pagination=pagination)