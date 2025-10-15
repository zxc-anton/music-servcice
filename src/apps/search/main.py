from fastapi import APIRouter


router = APIRouter( tags=["search"])

from src.apps.search import routers