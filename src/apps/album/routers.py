from src.apps.album.main import router
from src.apps.album.depenency import service
from src.apps.album.schemas import Album_Response, Album_Tracks_Response


@router.get("/{ID}")
async def get_album(service: service, ID: int) -> Album_Response:
    return await service.get_album(ID=ID)

@router.get("/{ID}/tracks")
async def get_album_tracks(service: service, ID: int) -> Album_Tracks_Response:
    return await service.get_album_tracks(ID=ID) 