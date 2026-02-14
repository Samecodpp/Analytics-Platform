from sqlalchemy import update

from ..models import Users
from .base_repo import BaseRepository

class UserRepository(BaseRepository):
    def get_by_id(self, id: int) -> Users | None:
        return self.session.get(Users, id)

    def update_by_id(self, id: int, fields: dict) -> Users | None:
        stmt = update(Users).where(Users.id == id).values(**fields).returning(Users)
        user = self.session.scalar(stmt)
        return user

