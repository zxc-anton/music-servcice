from fastapi import FastAPI
from starlette_admin.contrib.sqla import Admin, ModelView
from core.db.db_dependency.connect_db import get_engine
from database.models import User

def setup_admin(app: FastAPI): 
    admin = Admin(engine=get_engine())
    admin.add_view(ModelView(User))
    admin.mount_to(app)