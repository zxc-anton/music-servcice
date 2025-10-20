from src.apps.playlist.main import router
from src.apps.playlist.dependecy import service

@router.get("/{ID}/tracks")
async def get_playlist_tracks(ID: int, service: service): 
    return await service.get_playlist_tracks(ID=ID)