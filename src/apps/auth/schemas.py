from pydantic import BaseModel, Field, EmailStr, HttpUrl
from enum import Enum
from datetime import datetime, timedelta, timezone

from settings.setting import settings


class TokenType(Enum):
    access = "access_token"
    refresh = "refresh_token"


class NameField(BaseModel):
    name: str = Field(max_length=30, min_length=3)

class PasswordField(BaseModel):
    password: str

class ID_Field(BaseModel):
    ID: int = Field(ge=0)

class EmailField(BaseModel):
    email: EmailStr = Field(max_length=125, min_length=5)

class ReguesterUser(EmailField, NameField, PasswordField, BaseModel):
    """Схема данных для регистрации пользователя."""
    pass



class CreateUser(EmailField, NameField, BaseModel):
    """Схема данных для создания пользователя в базе данных."""
    password_hash: str
    

    
class TokenData(ID_Field, BaseModel):
    """Схема данных для создания access или refresh токена"""
    token_type: TokenType

    @property
    def expire(self) -> datetime:
        tdl = (timedelta(seconds=settings.access_token_expries) if self.token_type==TokenType.access
                else timedelta(seconds=settings.access_token_expries))
        return datetime.now(timezone.utc) + tdl

class UserResponse(ID_Field, NameField, BaseModel):
    """Схема данных пользователя для ответа."""
    avatar_url: HttpUrl | None 


class LoginUser(EmailField, PasswordField, BaseModel): 
    """Схема данных для входа пользователя."""
    pass

class PaginationParams(BaseModel):
    """Схема даанных для пагинаии контента."""
    limit: int = Field(10, gt=0, lt=200)
    offset: int = Field(0, ge=0)

