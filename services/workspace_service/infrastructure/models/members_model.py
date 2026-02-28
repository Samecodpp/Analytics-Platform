from datetime import datetime
from uuid import UUID, uuid4
from sqlalchemy import ForeignKey, DateTime, Enum as SAEnum, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ...domain.value_objects import Role
from ..core.database import Base


class MembersModel(Base):
    __tablename__ = "member"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    user_id: Mapped[UUID] = mapped_column(nullable=False)
    project_id: Mapped[UUID] = mapped_column(
        ForeignKey("project.id", ondelete="CASCADE"), nullable=False
    )
    invited_by: Mapped[UUID] = mapped_column(nullable=True)
    role: Mapped[Role] = mapped_column(SAEnum(Role, name="role_enum"), nullable=False)
    joined_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    project = relationship("ProjectsModel", back_populates="members")
    permissions = relationship(
        "Permission", back_populates="member", cascade="all, delete-orphan"
    )
