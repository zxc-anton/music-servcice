from fastapi import APIRouter

router = APIRouter(prefix="/user", tags=["user"])

from src.apps.user import routers