from fastapi import APIRouter
from src.apps.auth.main import router as auth_router
from src.apps.track.main import router as track_router
from src.apps.user.main import router as user_router
from src.apps.search.main import router as search_router


router = APIRouter(prefix=("/api"))
router.include_router(auth_router)
router.include_router(track_router)
router.include_router(user_router)
router.include_router(search_router)