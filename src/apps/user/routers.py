from src.apps.user.main import router
from src.apps.user.dependency import service, current_user, pagination




@router.get("/listen_history")
async def get_listen_history(service: service, user: current_user, params: pagination):
    return await service.get_listen_history(params=params, user=user)