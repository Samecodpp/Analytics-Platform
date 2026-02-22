from __future__ import annotations
from datetime import datetime
from typing import List, TYPE_CHECKING
from uuid import UUID, uuid4
from sqlalchemy import Index, DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..core.database import Base

if TYPE_CHECKING:
    from .refresh_tokens_model import RefreshTokenModel


class CredentialsModel(Base):
    __tablename__ = "credential"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    refresh_tokens: Mapped[List["RefreshTokenModel"]] = relationship(back_populates="credential")

    __table_args__ = (Index("idx_cred_email", "email", postgresql_using="hash"),)
