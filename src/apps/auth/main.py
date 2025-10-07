from fastapi import APIRouter


router = APIRouter(prefix="/auth", tags=["auth"])


from src.apps.auth import routers
