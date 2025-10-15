from urllib import response
from pydantic import Json
from src.apps.auth.manager import Manager
from src.apps.auth.handlers import Handlers
from fastapi import Depends, HTTPException
from src.apps.auth.schemas import ( ReguesterUser, CreateUser, 
                                    LoginUser, 
                                    TokenData, TokenType)
from src.schemas import ID_Field, EmailField, UserResponse
from src.apps.auth.tasks import send_verify_email
from fastapi.responses import JSONResponse
from settings.setting import settings
from typing import Annotated


class Service:
    def __init__(self, manager: Annotated[Manager, Depends(Manager)], handlers: Annotated[Handlers, Depends(Handlers)]):
        self.manager: Manager = manager
        self.handlers: Handlers = handlers
        

    async def create_user(self, user: ReguesterUser) -> None:
        password_hash = await self.handlers.get_hashed_password(user.password)
        new_user = CreateUser(name=user.name, email=user.email, password_hash=password_hash)
        await self.manager.create_user(new_user)
        token = await self.handlers.create_verify_token(email=user.email)
        send_verify_email.delay(user.email, token)

    async def get_user_by_id(self, ID: ID_Field) -> UserResponse:
        return await self.manager.get_user_by_id(ID=ID)

    async def confirm_user(self, token: str) -> None:
        email = await self.handlers.load_verify_token(token)
        await self.manager.confirm_user(email)
        
    async def get_user_by_email(self, email: EmailField) -> UserResponse:
        return await self.manager.get_user_by_email(email)

    async def login(self, login_user: LoginUser) -> JSONResponse:
        hash_password = await self.manager.get_user_password(login_user.email)
        
        if hash_password is None:
            raise HTTPException(401)
        result = await self.handlers.compare_passwords(login_user.password, hash_password)
        if result is False:
            raise HTTPException(401, "Password or email is incorrect")
        user = await self.manager.get_user_by_email(login_user.email)
        access_token = await self.handlers.create_token(TokenData(token_type=TokenType.access, ID=user.ID))
        refresh_token = await self.handlers.create_token(TokenData(token_type=TokenType.refresh, ID=user.ID))
        response = JSONResponse(content={"message": "User confirm."})
        response.set_cookie(key="access_token", httponly=True, value=access_token, expires=settings.expries_cookie)
        response.set_cookie(key="refresh_token", httponly=True, value=refresh_token, expires=settings.expries_cookie)
        return response
    
    async def update_token(self, refresh_token: str) -> JSONResponse:
        payload = await self.handlers.decode_token(refresh_token)
        if payload["type"] != TokenType.refresh.value:
            raise HTTPException(401, "Token not invalid")
        token = await self.handlers.create_token(TokenData(ID=payload['sub'], token_type=TokenType.access))
        response = JSONResponse(content={"message": "token was updated."})        
        response.set_cookie("access_token", value=token, expires=settings.expries_cookie, httponly=True)
        return response
    
    async def logout(self) -> JSONResponse:
        response = JSONResponse(content={"message": "logout."})
        response.delete_cookie(TokenType.access.value)
        response.delete_cookie(TokenType.refresh.value)
        return response

        

