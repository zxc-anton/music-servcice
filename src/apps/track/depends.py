from fastapi import Depends
from typing import Annotated



from src.apps.track.manager import Manager
manager = Annotated[Manager, Depends(Manager)]

from src.apps.track.service import Service
service = Annotated[Service, Depends(Service)]

