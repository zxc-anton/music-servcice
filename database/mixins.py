import sqlalchemy.orm as so
import sqlalchemy as sa
from datetime import datetime, timezone


class ID_mixin:
    ID: so.Mapped[int] = so.mapped_column(sa.Integer, primary_key=True, index=True, autoincrement=True)

class CREATED_AT_mixin:
    created_at: so.Mapped[datetime] = so.mapped_column(sa.DateTime(timezone=True), server_default=sa.func.now())

class UPDATED_AT_mixin:
    updated_at: so.Mapped[datetime] = so.mapped_column(sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now())

class TIMESTAMP_mixin(CREATED_AT_mixin, UPDATED_AT_mixin):
    pass