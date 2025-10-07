from pydantic import BaseModel, Field

class ID_Field(BaseModel):
    ID: int = Field(ge=0)

class Pagination(BaseModel):
    offset: int = Field(ge=0, default=0)
    limit: int = Field(ge=0, default=10, le=100)
 

