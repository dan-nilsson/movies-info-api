from datetime import UTC, datetime
from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(200), nullable=True)
    
    profile_art: Mapped[str | None] = mapped_column(
        String(200),
        nullable=True,
        default=None,
    )
    date_joined: Mapped[datetime] = mapped_column(DateTime(timezone=True),default=lambda: datetime.now(UTC))
    #liked: Mapped[list[Movie]] = relationship(back_populates='likes')

    @property
    def image_path(self) -> str:
        if self.profile_art:
            return f'/media/profile_pics/{self.profile_art}'
        return '/static/profile_pics/default.jpg'


class Movie(Base):
    __tablename__ = 'movies'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    director: Mapped[str] = mapped_column(String(100), nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    runtime: Mapped[int] = mapped_column(Integer, nullable=False)
    genre: Mapped[str] = mapped_column(String(50), nullable=False)
    rating: Mapped[float] = mapped_column(Float(precision=1), nullable=False)

    poster_art: Mapped[str | None] = mapped_column(
        String(200),
        nullable=True,
        default=None,
    )
    date_added: Mapped[datetime] = mapped_column(DateTime(timezone=True),default=lambda: datetime.now(UTC))
    #likes: Mapped[list[User]] = relationship(back_populates='liked')

    @property
    def image_path(self) -> str:
        if self.poster_art:
            return f'/media/poster_pics/{self.poster_art}'
        return '/static/poster_pics/default.jpg'
        