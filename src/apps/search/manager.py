from src.dependency import db
import sqlalchemy as sa
from database.models import Track, Author


class Manager:
    def __init__(self, db: db) -> None:
        self.db = db
        self.model = Track
        self.author_model = Author

    async def search(self, q: str):
        query = (sa.select( self.author_model, self.model)
                 .join(self.author_model, self.model.authors)
                 .filter(sa.or_(self.model.title.ilike(q),
                                self.author_model.name.ilike(q))))
        async with self.db.get_session() as session:
            result = await session.execute(query)
        return result.mappings().all()
