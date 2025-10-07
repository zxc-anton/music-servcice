from src.apps.user.dependency import db
from src.apps.auth.schemas import ID_Field
from src.apps.track.schemas import Pagination
from database.models import Track, Author, User
import sqlalchemy as sa
from database.association_tables import Listen_History



class Manager:
    def __init__(self, db: db) -> None:
        self.db = db
        self.model = Track
        self.author_model = Author
        self.user_model = User
        self.listen_history = Listen_History

    async def get_listen_history(self, params: Pagination, ID: ID_Field):
        query = (sa.select(self.model.ID, self.model.title, self.model.file_url, self.listen_history.c.track_ID, self.listen_history.c.listened_at, self.author_model.ID,
                           self.author_model.name, self.author_model.photo_url)
                 .join(self.user_model, self.user_model.ID == self.listen_history.c.user_ID)
                 .join(self.author_model, self.model.authors)
                 .where(self.user_model.ID == ID)
                 .order_by(sa.desc(self.listen_history.c.listened_at))
                 .offset(params.offset)
                 .limit(params.limit))
        async with self.db.get_session() as session:
            result = await session.execute(query)
        return result.mappings().all()