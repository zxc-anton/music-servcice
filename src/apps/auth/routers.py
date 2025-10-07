from src.apps.auth.main import router
from src.apps.auth.schemas import ReguesterUser, UserResponse, LoginUser
from fastapi import Depends, Cookie
from src.apps.auth.dependency import service, get_current_user
from typing import Annotated
from fastapi.responses import JSONResponse



@router.post("/users/", status_code=201, response_model=dict[str, str])
async def create_user(user: ReguesterUser, service: service):
    """
    Созаать пользователя в базе данных.
    """
    await service.create_user(user)
    return {"message": "User created."}


@router.get("/confirm_user", status_code=200, response_model=dict[str, str])
async def confirm_user(token: str, service: service):
    """Подтвердить регистраацию пользователя."""
    await service.confirm_user(token=token)
    return {"message": "user was confirm"}
     
@router.post("/login", status_code=200)
async def user_login(user: LoginUser, service: service) -> JSONResponse:
    """Вход пользователя в аккаунт"""
    return await service.login(user)

@router.get("/current_user", status_code=200)
async def current_user(current_user: Annotated[UserResponse, Depends(get_current_user)]):
    """Получить текущего пользователя."""
    return current_user

@router.get("/update_token")
async def update_token(refresh_token: Annotated[str, Cookie()], service: service) -> JSONResponse:
    """Обновить токен."""
    return await service.update_token(refresh_token)

@router.post("/logout")
async def logout(service: service) -> JSONResponse:
    """Выйти из аккаунта."""
    return await service.logout()
    
