from src.apps.artist.main import router
from src.apps.artist.dependency import service
from src.dependency import pagination
from src.apps.artist.schemas import Artist_Response, Albums_Response



@router.get("/{ID}")
async def get_artist(ID: int, service: service) -> Artist_Response:
    return await service.get_artist(ID)

@router.get("/{ID}/albums")
async def get_artist_albums(ID: int, service: service, pagination: pagination) -> Albums_Response:
    return await service.get_artist_albums(ID=ID, pagination=pagination)


@router.get("/{ID}/popular_tracks")
async def get_artist_popular_track(ID: int, service: service, pagination: pagination):
    return await service.get_artist_popular_track(ID=ID, pagination=pagination)