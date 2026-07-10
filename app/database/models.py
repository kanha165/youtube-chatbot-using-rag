from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    TIMESTAMP
)

from sqlalchemy.sql import func
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Video(Base):

    __tablename__ = "videos"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    video_id = Column(
        String(100),
        nullable=False
    )

    video_url = Column(
        Text,
        nullable=False
    )

    title = Column(
        String(500)
    )

    created_at = Column(
        TIMESTAMP,
        server_default=func.now()
    )