from fastapi import APIRouter

router = APIRouter(prefix="/stream", tags=["stream"])

from src.apps.stream_servic import routers
