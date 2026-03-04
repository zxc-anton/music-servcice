
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.apps.main import router
from fastapi.responses import ORJSONResponse
from src.apps.admin.admin_base import setup_admin



app = FastAPI(
    default_response_class=ORJSONResponse,
    title="music-servic"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True
)

app.include_router(router)
setup_admin(app)
