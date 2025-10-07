from sqlalchemy.orm import DeclarativeBase, declared_attr
from database.mixins import ID_mixin, TIMESTAMP_mixin
import sqlalchemy.orm as so
import sqlalchemy as sa
from typing import Annotated

path_str = Annotated[str, so.mapped_column(sa.String, unique=True, nullable=True)]


class Base(DeclarativeBase):
    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
    
from database.association_tables import favorites, Track_Artist, Album_Author, Playlist_Track, Listen_History
    
class User(ID_mixin, TIMESTAMP_mixin, Base):
    name: so.Mapped[str] = so.mapped_column(sa.String(length=30), nullable=False)
    email: so.Mapped[str] = so.mapped_column(sa.String(length=125), unique=True, index=True)
    password_hash: so.Mapped[str] = so.mapped_column(nullable=False)
    is_superuser: so.Mapped[bool] = so.mapped_column(default=False, nullable=False, server_default="'false'")
    avatar_url: so.Mapped[str | None] = so.mapped_column(nullable=True)
    is_verification: so.Mapped[bool] = so.mapped_column(nullable=False, default=False)

    posts: so.Mapped[list["Playlist"]] = so.relationship("Playlist", back_populates="user", cascade="all, delete-orphan")
    tracks: so.Mapped[list["Track"]] = so.Relationship("Track", secondary=favorites, back_populates="users")
    listening_songs: so.Mapped[list["Track"]] = so.relationship("Track", secondary=Listen_History, back_populates="listening_users")

class Track(TIMESTAMP_mixin, ID_mixin,  Base):
    title: so.Mapped[str] = so.mapped_column(sa.String, nullable=False, index=True)
    file_url: so.Mapped[path_str]
    
    users: so.Mapped[list["User"]] = so.relationship("User", secondary=favorites, back_populates="tracks")
    authors: so.Mapped[list["Author"]] = so.relationship("Author", secondary=Track_Artist, back_populates="tracks")
    playlists: so.Mapped[list["Playlist"]] = so.relationship("Playlist", secondary=Playlist_Track, back_populates="tracks")
    listening_users: so.Mapped[list["User"]] = so.relationship("User", secondary=Listen_History, back_populates="listening_songs")

class Author(TIMESTAMP_mixin, ID_mixin, Base):
    name: so.Mapped[str] = so.mapped_column(sa.String, nullable=False, index=True)
    photo_url: so.Mapped[path_str]

    tracks: so.Mapped[list["Track"]] = so.relationship("Track", secondary=Track_Artist, back_populates="authors")
    albums: so.Mapped[list["Album"]] = so.relationship("Album", secondary=Album_Author, back_populates="authors")

class Album(TIMESTAMP_mixin, ID_mixin, Base):
    title: so.Mapped[str] = so.mapped_column(sa.String, nullable=False, index=True)
    cover_url: so.Mapped[path_str]

    authors: so.Mapped[list["Author"]] = so.relationship("Author", secondary=Album_Author, back_populates="albums")

class Playlist(TIMESTAMP_mixin, ID_mixin, Base):
    name: so.Mapped[str] = so.mapped_column(sa.String, nullable=False)
    cover_url: so.Mapped[str | None] = so.mapped_column(unique=True, nullable=True)
    is_public: so.Mapped[bool] = so.mapped_column(sa.Boolean, default=True, server_default="'true")
    user_ID: so.Mapped[int] = so.mapped_column(sa.ForeignKey("user.ID"))

    user: so.Mapped["User"] = so.relationship("User", back_populates="posts")
    tracks: so.Mapped[list["Track"]] = so.relationship("Track", secondary=Playlist_Track, back_populates="playlists")