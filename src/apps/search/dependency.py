from core.db.db_dependency.connect_db import DB_dependency
from typing import Annotated
from fastapi import Depends

db = Annotated[DB_dependency, Depends(DB_dependency)]

from src.apps.search.manager import Manager
manager = Annotated[Manager, Depends(Manager)]

from src.apps.search.service import Service
service = Annotated[Service, Depends(Service)]