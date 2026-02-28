from datetime import datetime
from uuid import UUID, uuid4
from sqlalchemy import (
    ForeignKey,
    DateTime,
    Enum as SAEnum,
    Boolean,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ...domain.value_objects import EPermission
from ..core.database import Base


class Permission(Base):
    __tablename__ = "permission"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    member_id: Mapped[UUID] = mapped_column(
        ForeignKey("member.id", ondelete="CASCADE"), nullable=False
    )
    permission: Mapped[EPermission] = mapped_column(
        SAEnum(EPermission, name="permission_enum"), nullable=False
    )
    granted: Mapped[bool] = mapped_column(Boolean, nullable=False)
    granted_by: Mapped[UUID] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    member = relationship("MembersModel", back_populates="permissions")
