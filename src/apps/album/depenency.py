from typing import Annotated
from fastapi import Depends


from src.apps.album.manager import Manager
manager = Annotated[Manager, Depends(Manager)]


from src.apps.album.service import Service
service = Annotated[Service, Depends(Service)]