from fastapi import Depends

from core.db.db_dependency.connect_db import DB_dependency
from database.models import User
import sqlalchemy as sa


class ProfileManager:
    def __init__(self, db: DB_dependency = Depends(DB_dependency)) -> None:
        self._db: DB_dependency = db
        self._model = User

    async def update_fields(self, id: int, **kwargs):
        query = sa.update(self._model).where(self._model.ID == id).values(**kwargs)

        async with self._db.get_session() as session: 
            await session.execute(query)
            await session.commit()

    async def get_user_passwords(self, id: int) -> str | None:
        query = sa.select(self._model.password_hash).where(self._model.ID == id)
        async with self._db.get_session() as session:
            result = await session.execute(query)
        return result.scalar()



            