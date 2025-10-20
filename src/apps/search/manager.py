from src.dependency import db
import sqlalchemy as sa
from database.models import Track, Author


class Manager:
    def __init__(self, db: db) -> None:
        self.db = db
        self.model = Track
        self.author_model = Author

    async def search(self, q: str):
        query = (sa.select(self.model.title).filter(self.model.title.ilike(q)))
                 
        async with self.db.get_session() as session:
            result = await session.execute(query)
        return result.mappings().all()
