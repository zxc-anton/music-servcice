from fastapi import Depends
from typing import Annotated



from src.apps.user.manager import Manager
manager = Annotated[Manager, Depends(Manager)]

from src.apps.user.service import Service
service = Annotated[Service, Depends(Service)]
