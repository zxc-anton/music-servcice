from fastapi import Cookie, Depends, HTTPException
from src.apps.auth.service import Service
from src.apps.auth.manager import Manager
from typing import Annotated
from src.apps.auth.schemas import UserResponse
from src.apps.auth.schemas import TokenType


service = Annotated[Service, Depends(Service)]
manager = Annotated[Manager, Depends(Manager)]


async def get_current_user(service: service,
                     access_token: Annotated[str, Cookie] = Cookie()) -> UserResponse: 
    payload = await service.handlers.decode_token(access_token)
    print(payload["type"])
    if payload["type"] != TokenType.access.value:
        raise HTTPException(401, "Not valid token")
    user = await service.get_user_by_id(payload["sub"])
    return user
    
    

