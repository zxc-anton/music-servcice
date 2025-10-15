from src.apps.me.main import router
from src.apps.user.dependency import service as user_service
from src.apps.me.dependency import service
from src.dependency import current_user, pagination
from src.schemas import ID_Field
from src.apps.me.schemas import Playlist

@router.get("/")
async def get_me(service: user_service, user: current_user): 
    return await service.get_user(ID=user.ID)

@router.get("/favorits")
async def get_my_favorits(service: user_service, user: current_user, pagination: pagination):
    return await service.get_favorits(ID=user.ID, pagination=pagination)

@router.get("/playlists")
async def get_my_playlists(service: user_service, user: current_user, pagination: pagination):
    return await service.get_playlists(ID=user.ID, pagination=pagination)

@router.get("/listen_history")
async def get_listen_history(service: user_service, user: current_user, pagination: pagination):
    return await service.get_listen_history(ID=user.ID, pagination=pagination)
    
@router.post("/favorites", status_code=201)
async def add_in_favorites(service: service, user: current_user, track_ID: ID_Field):
    return await service.add_in_favorites(track_ID=track_ID, user_ID=user.ID)

@router.post("/playlist", status_code=201)
async def create_playlist(service: service, user: current_user, playlist: Playlist):
    return await service.create_playlist(user_ID=user.ID, playlist=playlist)

@router.patch("/playlist")
async def add_track_in_playlist(service: service, user: current_user):
    pass