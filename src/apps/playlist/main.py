from fastapi import APIRouter

router = APIRouter(prefix="/playlists", tags=["playlist"])

from src.apps.playlist import routers