from pydantic import BaseModel, EmailStr, StringConstraints
from typing import Annotated

class NewEmail(BaseModel):
    email: EmailStr

class NewPassword(BaseModel):
    old_password: Annotated[str, StringConstraints(min_length=5, max_length=128)]
    new_password: Annotated[str, StringConstraints(min_length=5, max_length=128)]