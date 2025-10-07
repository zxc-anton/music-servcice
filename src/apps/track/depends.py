from fastapi import Depends, Query
from core.db.db_dependency.connect_db import DB_dependency
from typing import Annotated
from src.apps.track.schemas import Pagination

db = Annotated[DB_dependency, Depends(DB_dependency)]

from src.apps.track.manager import Manager
manager = Annotated[Manager, Depends(Manager)]

from src.apps.track.service import Service
service = Annotated[Service, Depends(Service)]

pagination = Annotated[Pagination, Query()]