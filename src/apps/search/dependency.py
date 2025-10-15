from typing import Annotated
from fastapi import Depends


from src.apps.search.manager import Manager
manager = Annotated[Manager, Depends(Manager)]

from src.apps.search.service import Service
service = Annotated[Service, Depends(Service)]