from src.apps.album.main import router
from src.apps.album.depenency import service
from src.schemas import ID_Field


@router.get("/{ID}")
async def get_album(service: service, ID: int):
    return await service.get_album(ID=ID)

@router.get("/{ID}/tracks")
async def get_album_tracks(service: service, ID: int):
    return await service.get_album_tracks(ID=ID)