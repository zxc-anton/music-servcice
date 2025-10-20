from src.apps.auth.manager import Manager
from src.apps.auth.handlers import Token_Handlers, Password_Handlers
from src.apps.auth.dependency import manager, password_handlers, token_handlers
from fastapi import Depends, HTTPException
from src.apps.auth.schemas import ( ReguesterUser, CreateUser, 
                                    LoginUser, 
                                    TokenData, TokenType)
from src.schemas import ID_Field, Email_Field, User_DTO, User_Response
from src.apps.auth.tasks import send_verify_email
from fastapi.responses import ORJSONResponse
from settings.setting import settings
from typing import Annotated


class Service:
    def __init__(self, manager: manager, password_handlers: password_handlers, token_handlers: token_handlers):
        self.manager: Manager = manager
        self.password_handlers: Password_Handlers = password_handlers
        self.token_handlers: Token_Handlers = token_handlers
        

    async def create_user(self, user_data: ReguesterUser) -> User_Response:
        password_hash = await self.password_handlers.get_hashed_password(user_data.password)
        new_user = CreateUser(name=user_data.name, email=user_data.email, password_hash=password_hash)
        user = await self.manager.create_user(new_user)
        token = await self.token_handlers.create_verify_token(email=user_data.email)
        send_verify_email.delay(user_data.email, token)
        return user

    async def get_user_by_id(self, ID: ID_Field) -> User_DTO:
        return await self.manager.get_user_by_id(ID=ID)

    async def confirm_user(self, token: str) -> None:
        email = await self.token_handlers.load_verify_token(token)
        await self.manager.confirm_user(email)
        
    async def get_user_by_email(self, email: Email_Field) -> User_DTO:
        return await self.manager.get_user_by_email(email)

    async def login(self, login_user: LoginUser) -> ORJSONResponse:
        hash_password = await self.manager.get_user_password(login_user.email)
        
        if hash_password is None:
            raise HTTPException(401, "User not found")
        result = await self.password_handlers.compare_passwords(login_user.password, hash_password)
        if result is False:
            raise HTTPException(401, "Password or email is incorrect")
        user = await self.manager.get_user_by_email(login_user.email)
        access_token = await self.token_handlers.create_token(TokenData(token_type=TokenType.access, ID=user.ID))
        refresh_token = await self.token_handlers.create_token(TokenData(token_type=TokenType.refresh, ID=user.ID))
        response = ORJSONResponse(content={"message": "User confirm."})
        response.set_cookie(key="access_token", httponly=True, value=access_token, expires=settings.expries_cookie)
        response.set_cookie(key="refresh_token", httponly=True, value=refresh_token, expires=settings.expries_cookie)
        return response
    
    async def update_token(self, refresh_token: str) -> ORJSONResponse:
        payload = await self.token_handlers.decode_token(refresh_token)
        if payload["type"] != TokenType.refresh.value:
            raise HTTPException(401, "Token not invalid")
        token = await self.token_handlers.create_token(TokenData(ID=payload['sub'], token_type=TokenType.access))
        response = ORJSONResponse(content={"message": "token was updated."})        
        response.set_cookie("access_token", value=token, expires=settings.expries_cookie, httponly=True)
        return response
    
    async def logout(self) -> ORJSONResponse:
        response = ORJSONResponse(content={"message": "logout."})
        response.delete_cookie(TokenType.access.value)
        response.delete_cookie(TokenType.refresh.value)
        return response

        

