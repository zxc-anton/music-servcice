from fastapi import APIRouter
from src.apps.auth.main import router as auth_router
from src.apps.track.main import router as track_router
from src.apps.user.main import router as user_router
from src.apps.search.main import router as search_router
from src.apps.album.main import router as album_router
from src.apps.artist.main import router as artist_router
from src.apps.me.main import router as me_router
from src.apps.stream_servic.main import router as stream_router


router = APIRouter(prefix=("/api"))
router.include_router(auth_router)
router.include_router(track_router)
router.include_router(user_router)
router.include_router(search_router)
router.include_router(album_router)
router.include_router(artist_router)
router.include_router(me_router)
router.include_router(stream_router)