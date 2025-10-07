from unittest import result
from src.apps.search.dependency import db
import sqlalchemy as sa
from database.models import Track


class Manager:
    def __init__(self, db: db) -> None:
        self.db = db
        self.model = Track

    async def search(self, q: str):
        query = sa.select(self.model.ID, self.model.title).where(self.model.title.ilike(q))
        async with self.db.get_session() as session:
            result = await session.execute(query)
        return result.mappings().all()
