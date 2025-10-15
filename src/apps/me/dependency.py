from typing import Annotated
from fastapi import Depends


from src.apps.me.manager import Manager
manager = Annotated[Manager, Depends(Manager)]


from src.apps.me.service import Service
service = Annotated[Service, Depends(Service)]
