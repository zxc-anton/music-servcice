from src.apps.auth.main import router
from src.apps.auth.schemas import ReguesterUser, LoginUser
from src.apps.auth.dependency import refresh_token
from src.apps.auth.dependency import service
from src.schemas import User_Response
from fastapi.responses import ORJSONResponse
from src.dependency import current_user



@router.post("/users/", status_code=201)
async def create_user(user: ReguesterUser, service: service) -> User_Response:
    """
    Созаать пользователя в базе данных.
    """
    return await service.create_user(user)


@router.get("/confirm_user", status_code=200)
async def confirm_user(token: str, service: service) -> dict[str, str]:
    """Подтвердить регистраацию пользователя."""
    await service.confirm_user(token=token)
    return {"message": "user was confirm"}
     
@router.post("/login", status_code=204)
async def user_login(user: LoginUser, service: service) -> ORJSONResponse:
    """Вход пользователя в аккаунт"""
    return await service.login(user)

@router.get("/current_user", status_code=200)
async def current_user(current_user: current_user) -> User_Response:
    """Получить текущего пользователя."""
    return current_user

@router.post("/update_token")
async def update_token(refresh_token: refresh_token, service: service) -> ORJSONResponse:
    """Обновить токены."""
    return await service.update_token(refresh_token)

@router.post("/logout")
async def logout(service: service) -> ORJSONResponse:
    """Выйти из аккаунта."""
    return await service.logout()
    
