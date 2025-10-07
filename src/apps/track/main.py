from fastapi import APIRouter

router = APIRouter(prefix="/track", tags=["track"])

from src.apps.track import routers