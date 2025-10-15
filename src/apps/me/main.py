from fastapi import APIRouter

router = APIRouter(prefix="/me", tags=["me"])

from src.apps.me import routers