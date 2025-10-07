from fastapi import Depends, Query
from core.db.db_dependency.connect_db import DB_dependency
from typing import Annotated
from src.apps.track.schemas import Pagination
from src.apps.auth.dependency import get_current_user
from src.apps.auth.schemas import UserResponse

db = Annotated[DB_dependency, Depends(DB_dependency)]

from src.apps.user.manager import Manager
manager = Annotated[Manager, Depends(Manager)]

from src.apps.user.service import Service
service = Annotated[Service, Depends(Service)]


current_user = Annotated[UserResponse, Depends(get_current_user)]
pagination = Annotated[Pagination, Query()]