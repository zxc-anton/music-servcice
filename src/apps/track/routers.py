from src.apps.track.main import router
from src.apps.track.depends import service
from src.dependency import pagination
from src.schemas import ID_Field
from src.apps.track.schemas import  Popular_Tracks_Schema



@router.get("/popular")
async def get_popular_tracks(params: pagination, service: service):
    return await service.get_popular_tracks(params=params)

@router.get("/{ID}")
async def get_track_by_ID(ID: int, service: service):
    return await service.get_track_by_id(ID=ID_Field(ID=ID))




