from fastapi import APIRouter


router = APIRouter(prefix="/albums", tags=["album"])

from src.apps.album import routers