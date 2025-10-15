from fastapi import APIRouter

router = APIRouter(prefix="/artists", tags=["artist"])


from src.apps.artist import routers