from fastapi import APIRouter

router = APIRouter(prefix="/profile", tags=["profile"])

from src.apps.profile import routers