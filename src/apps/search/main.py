from fastapi import APIRouter


router = APIRouter(prefix="/search", tags=["search"])

from src.apps.search import routers