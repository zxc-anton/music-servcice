from src.apps.track.main import router
from src.apps.track.depends import service
from src.dependency import pagination



@router.get("/popular")
async def get_popular_tracks(params: pagination, service: service):
    return await service.get_popular_tracks(params=params)

@router.get("/{ID}")
async def get_track_by_ID(ID: int, service: service):
    return await service.get_track_by_id(ID=ID)




