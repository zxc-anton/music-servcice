from src.apps.playlist.manager import Manager
from typing import Annotated
from fastapi import Depends


manager = Annotated[Manager, Depends(Manager)]


from src.apps.playlist.service import Service

service = Annotated[Service, Depends(Service)]