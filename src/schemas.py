from pydantic import BaseModel, Field, EmailStr, HttpUrl, ConfigDict
from database.models import User

class Links(BaseModel):
    self: HttpUrl

class Name_Field(BaseModel):
    name: str = Field(max_length=30, min_length=3)

class Password_Field(BaseModel):
    password: str

class ID_Field(BaseModel):
    ID: int = Field(ge=0)

class Email_Field(BaseModel):
    email: EmailStr = Field(max_length=125, min_length=5)

class User_DTO(ID_Field, Name_Field, BaseModel):
    """Схема данных пользователя для ответа."""
    avatar_url: HttpUrl | None = None
    model_config = ConfigDict(extra="ignore")

class Pagination_Params(BaseModel):
    """Схема даанных для пагинаии контента."""
    limit: int = Field(10, gt=0, lt=200)
    offset: int = Field(0, ge=0)

class User_Attributes(Name_Field, BaseModel): 
    avatar_url: HttpUrl | None = None
    model_config = ConfigDict(extra="ignore")

class User_Relationships(BaseModel): 
    pass

class User_Schema(ID_Field, BaseModel): 
    type: str = User.__name__
    attributes: User_Attributes
    relationships: User_Relationships | None = None

class User_Response(BaseModel):
    data: User_Schema
    model_config = ConfigDict(extra="ignore")