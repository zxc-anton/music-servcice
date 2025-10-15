from fastapi import APIRouter

router = APIRouter(prefix="/users", tags=["user"])

from src.apps.user import routers