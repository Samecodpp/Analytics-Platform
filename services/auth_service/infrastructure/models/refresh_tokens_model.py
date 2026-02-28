from __future__ import annotations
from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID
from sqlalchemy import DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..core.database import Base

if TYPE_CHECKING:
    from .credentials_model import CredentialsModel


class RefreshTokenModel(Base):
    __tablename__ = "refresh_token"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    creds_id: Mapped[UUID] = mapped_column(
        ForeignKey("credential.id", ondelete="CASCADE")
    )
    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    revoked_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    credential: Mapped["CredentialsModel"] = relationship(
        back_populates="refresh_tokens"
    )
