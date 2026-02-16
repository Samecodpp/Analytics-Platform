from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import DateTime, Boolean, ForeignKey, Enum as SQLEnum
from datetime import datetime, timezone
from ..core.database import Base
import enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .users_model import Users
    from .project_model import Projects


class ProjectRole(str, enum.Enum):
    OWNER = "owner"
    API_MASTER = "api-master"
    ANALYST = "analyst"
    VIEWER = "viewer"


class Memberships(Base):
    __tablename__ = "membership"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE"), nullable=False
    )
    project_id: Mapped[int] = mapped_column(
        ForeignKey("project.id", ondelete="CASCADE"), nullable=False
    )
    role: Mapped[ProjectRole] = mapped_column(SQLEnum(ProjectRole), nullable=False)
    is_invited: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    invited_by: Mapped[int | None] = mapped_column(
        ForeignKey("user.id", ondelete="SET NULL"), nullable=True
    )
    invited_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc)
    )

    user: Mapped["Users"] = relationship(
        back_populates="memberships", foreign_keys=[user_id]
    )
    project: Mapped["Projects"] = relationship(back_populates="memberships")
    inviter: Mapped["Users"] = relationship(foreign_keys=[invited_by], lazy="selectin")

    def __repr__(self) -> str:
        return f"Membership(id={self.id!r}, user_id={self.user_id!r}, project_id={self.project_id!r}, role={self.role!r})"
