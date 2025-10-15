from fastapi import Depends, HTTPException, Request
from src.apps.auth.service import Service
from src.apps.auth.manager import Manager
from typing import Annotated
from src.schemas import UserResponse
from src.apps.auth.schemas import TokenType
from src.apps.auth.schemas import TokenType


service = Annotated[Service, Depends(Service)]
manager = Annotated[Manager, Depends(Manager)]

async def get_access_token(request: Request) -> str:
    access_token = request.cookies.get(TokenType.access.value, None)
    if access_token is None:
        raise HTTPException(401, "Unauthori")
    return access_token

async def get_refresh_token(request: Request) -> str:
    refresh_token = request.cookies.get(TokenType.refresh.value, None)
    if refresh_token is None:
        raise HTTPException(401, "Unauthori")
    return refresh_token

    

access_token = Annotated[str, Depends(get_access_token)]
refresh_token = Annotated[str, Depends(get_refresh_token)]


async def get_current_user(service: service,
                     access_token: access_token) -> UserResponse: 
    payload = await service.handlers.decode_token(access_token)
    print(payload["type"])
    if payload["type"] != TokenType.access.value:
        raise HTTPException(401, "Not valid token")
    user = await service.get_user_by_id(payload["sub"])
    return user


    

