from pydantic import BaseModel, Field, EmailStr, HttpUrl

class NameField(BaseModel):
    name: str = Field(max_length=30, min_length=3)

class PasswordField(BaseModel):
    password: str

class ID_Field(BaseModel):
    ID: int = Field(ge=0)

class EmailField(BaseModel):
    email: EmailStr = Field(max_length=125, min_length=5)

class UserResponse(ID_Field, NameField, BaseModel):
    """Схема данных пользователя для ответа."""
    avatar_url: HttpUrl | None 

class PaginationParams(BaseModel):
    """Схема даанных для пагинаии контента."""
    limit: int = Field(10, gt=0, lt=200)
    offset: int = Field(0, ge=0)


