from src.apps.track.main import router
from src.apps.track.depends import service, pagination
from fastapi import Depends
from src.apps.auth.dependency import get_current_user
from typing import Annotated
from src.apps.auth.schemas import UserResponse



@router.get("/popular")
async def get_popular_tracks(params: pagination, service: service):
    return await service.get_popular_tracks(params=params)

@router.get("/{ID}")
async def get_track_by_ID(ID: int, service: service):
    return await service.get_track_by_id(ID=ID)




