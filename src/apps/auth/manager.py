from unittest import result
from fastapi import Depends, HTTPException
from core.db.db_dependency.connect_db import DB_dependency
from src.apps.auth.schemas import ID_Field, Email_Field
from src.schemas import User_DTO
import sqlalchemy as sa
from database.models import User
from sqlalchemy.exc import IntegrityError
from typing import Annotated
from sqlalchemy.exc import NoResultFound
from src.schemas import User_DTO, User_Response, User_Attributes, User_Schema
from src.apps.auth.schemas import CreateUser

class Manager:
    def __init__(self, db: Annotated[DB_dependency, Depends(DB_dependency)]):
        self.db: DB_dependency = db
        self.model = User

    async def create_user(self, user: CreateUser) -> User_Response:
        query = sa.insert(self.model).values(**user.model_dump()).returning(self.model)
        async with self.db.get_session() as session:
            transaction = await session.begin()
            try:
                result = await session.execute(query)
                user_data = result.scalar_one()
                response = User_Response(data=User_Schema(ID=user_data.ID, attributes=User_Attributes(name=user_data.name, avatar_url=user_data.avatar_url)))
            except IntegrityError:
                await transaction.rollback()
                raise HTTPException(409, detail="User was exists.")
            await transaction.commit()
            return response

    async def get_user_by_id(self, ID: ID_Field) -> User_DTO:
        query = (sa.select(self.model.ID, self.model.name, self.model.avatar_url).
                 where(self.model.ID == ID))
        async with self.db.get_session() as session:
            result = await session.execute(query)
            user = result.fetchone()
        if user is None:
            raise HTTPException(404, "User not found.")
        return User_DTO(ID=user.ID, avatar_url=user.avatar_url, name=user.name)
    

    
    async def get_user_by_email(self, email: Email_Field) -> User_DTO:
        query = (sa.select(self.model.ID, self.model.name, self.model.avatar_url).
                 where(self.model.email == email))
        async with self.db.get_session() as session:
            result = await session.execute(query)
            user = result.mappings().one()
        if user is None:
            raise HTTPException(404, "User not found")
        return User_DTO(**user)

    async def confirm_user(self, email: Email_Field):
        """Актиация аккаунта пользователя."""
        query = (sa.update(self.model).where(self.model.email==email).values(is_verification=True))
        async with self.db.get_session() as session:
            await session.execute(query)
            await session.commit()

    async def get_user_password(self, email: Email_Field) -> str:
        query = sa.select(self.model.password_hash).where(self.model.email == email)
        async with self.db.get_session() as session:
            result = await session.execute(query)
        try:
            password = result.mappings().one()
        except NoResultFound:
            raise HTTPException(404, "User not found.")
        return password["password_hash"]

    
            