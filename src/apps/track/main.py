from fastapi import APIRouter

router = APIRouter(prefix="/tracks", tags=["track"])

from src.apps.track import routers