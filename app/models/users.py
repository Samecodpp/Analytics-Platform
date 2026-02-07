from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, DateTime, Null
from datetime import datetime, timezone
from ..core.database import Base

class Users(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String, unique=True)
    first_name: Mapped[str] = mapped_column(String(50), nullable=True)
    last_name: Mapped[str] = mapped_column(String(50), nullable=True)
    hashed_password: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.username!r}, fullname={self.email!r}, created_at={self.created_at!r})"
