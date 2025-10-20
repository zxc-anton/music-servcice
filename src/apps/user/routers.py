from src.apps.user.main import router
from src.apps.user.dependency import service
from src.dependency import pagination
from src.schemas import ID_Field, User_Response
from src.apps.user.schemas import Listen_History_Response, Favorits_Response, Playlists_Response


@router.get("/{ID}")
async def get_user(ID: int, service: service) -> User_Response:
    """Получить пользователя по ID."""
    return await service.get_user(ID=ID_Field(ID=ID))


@router.get("/{ID}/listen_history")
async def get_listen_history(service: service, ID: int, pagination: pagination) -> Listen_History_Response:
    return await service.get_listen_history(pagination=pagination, ID=ID_Field(ID=ID))

@router.get("/{ID}/playlists")
async def get_playlists(service: service, ID: int, pagination: pagination) -> Playlists_Response:
    return await service.get_playlists(ID=ID_Field(ID=ID), pagination=pagination)

@router.get("/{ID}/favorits")
async def get_favorits(service: service, ID: int, pagination: pagination) -> Favorits_Response:
    return await service.get_favorits(ID=ID_Field(ID=ID), pagination=pagination)