from sqlalchemy import insert

from ..models import Memberships
from .base_repo import BaseRepository

class MembershipRepository(BaseRepository):
    def create(self, fields: dict) -> Memberships | None:
        stmt = insert(Memberships).values(**fields).returning(Memberships)
        new_member = self.session.scalar(stmt)
        self.session.flush()
        return new_member
