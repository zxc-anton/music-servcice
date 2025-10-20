from src.apps.auth.dependency import get_current_user
from fastapi import Depends, Query
from typing import Annotated
from src.schemas import Pagination_Params, User_Response
from core.db.db_dependency.connect_db import DB_dependency

current_user = Annotated[User_Response, Depends(get_current_user)]
pagination = Annotated[Pagination_Params, Query()]
db = Annotated[DB_dependency, Depends(DB_dependency)]