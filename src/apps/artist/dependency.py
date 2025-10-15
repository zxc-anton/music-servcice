from typing import Annotated
from fastapi import Depends


from src.apps.artist.manager import Manager
manager = Annotated[Manager, Depends(Manager)]

from src.apps.artist.service import Service
service = Annotated[Service, Depends(Service)]