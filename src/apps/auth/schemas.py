from pydantic import BaseModel, Field
from src.schemas import Name_Field, Email_Field, ID_Field, Password_Field
from enum import Enum
from datetime import datetime, timedelta, timezone

from settings.setting import settings


class TokenType(Enum):
    access = "access_token"
    refresh = "refresh_token"

class ReguesterUser(Email_Field, Name_Field, Password_Field, BaseModel):
    """Схема данных для регистрации пользователя."""
    pass



class CreateUser(Email_Field, Name_Field, BaseModel):
    """Схема данных для создания пользователя в базе данных."""
    password_hash: str
    

    
class TokenData(ID_Field, BaseModel):
    """Схема данных для создания access или refresh токена"""
    token_type: TokenType

    @property
    def expire(self) -> datetime:
        tdl = (timedelta(seconds=settings.access_token_expries) if self.token_type==TokenType.access.value
                else timedelta(seconds=settings.refresh_token_expries))
        return datetime.now(timezone.utc) + tdl




class LoginUser(Email_Field, Password_Field, BaseModel): 
    """Схема данных для входа пользователя."""
    pass



