import sqlalchemy.orm as so
import sqlalchemy as sa
from database.models import Base

favorites = sa.Table("favorites",
                     Base.metadata,
                     sa.Column("user_ID", sa.Integer(), sa.ForeignKey("user.ID"), nullable=True, primary_key=True),
                     sa.Column("track_ID", sa.Integer(), sa.ForeignKey("track.ID"), nullable=True, primary_key=True)
                     )

Track_Artist = sa.Table("track_artist",
                        Base.metadata,
                        sa.Column("track_ID", sa.Integer(), sa.ForeignKey("track.ID"), nullable=True),
                        sa.Column("author_ID", sa.Integer(), sa.ForeignKey("author.ID"), nullable=True)
                        )

Album_Author = sa.Table("album_author",
                        Base.metadata,
                        sa.Column("author_ID", sa.Integer(), sa.ForeignKey("author.ID"), nullable=True),
                        sa.Column("album_ID", sa.Integer(), sa.ForeignKey("album.ID"), nullable=True)
                        )

Album_Track = sa.Table("album_track",
                       Base.metadata,
                       sa.Column("album_ID", sa.Integer(), sa.ForeignKey("album.ID"), nullable=True),
                       sa.Column("track_ID", sa.Integer(), sa.ForeignKey("track.ID"), nullable=True)
                       )

Playlist_Track = sa.Table("playlist_track",
                          Base.metadata,
                          sa.Column("playlist_ID", sa.Integer(), sa.ForeignKey("playlist.ID")),
                          sa.Column("track_ID", sa.Integer(), sa.ForeignKey("track.ID"))
                          )

Listen_History = sa.Table("listen_history",
                          Base.metadata,
                          sa.Column("user_ID", sa.Integer(), sa.ForeignKey("user.ID"), nullable=True),
                          sa.Column("track_ID", sa.Integer(), sa.ForeignKey("track.ID"), nullable=True),
                          sa.Column("listened_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
                          sa.Column("listening_time", sa.Integer())
                          )




