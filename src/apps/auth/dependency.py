from fastapi import Depends, HTTPException, Request
from typing import Annotated
from src.apps.auth.schemas import TokenType
from src.schemas import User_Response, User_Attributes, User_Schema
from core.async_queue.celery_config import Celery_Dependency

celery_app: Celery_Dependency = Celery_Dependency()

from src.apps.auth.handlers import Token_Handlers, Password_Handlers
token_handlers = Annotated[Token_Handlers, Depends(Token_Handlers)]
password_handlers = Annotated[Password_Handlers, Depends(Password_Handlers)]


from src.apps.auth.manager import Manager
manager = Annotated[Manager, Depends(Manager)]

from src.apps.auth.service import Service
service = Annotated[Service, Depends(Service)]



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

async def get_token_payload(access_token: access_token, token_handlers: token_handlers) -> dict:
    return await token_handlers.decode_token(access_token)

async def get_current_user(service: service,
                     payload: Annotated[dict, Depends(get_token_payload)]) -> User_Response: 
    if payload["type"] != TokenType.access.value:
        raise HTTPException(401, "Not valid token")
    user = await service.get_user_by_id(ID=payload["sub"])
    return User_Response(data=User_Schema(ID=user.ID, attributes=User_Attributes(name=user.name, avatar_url=user.avatar_url)))


    

