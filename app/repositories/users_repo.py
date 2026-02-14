from sqlalchemy import update, select

from ..models import Users
from .base_repo import BaseRepository

class UserRepository(BaseRepository):
    def get_by_id(self, id: int) -> Users | None:
        return self.session.get(Users, id)

    def get_by_email(self, email: str) -> Users | None:
        stmt = select(Users).where(Users.email == email)
        return self.session.scalar(stmt)

    def update_by_id(self, id: int, fields: dict) -> Users | None:
        stmt = update(Users).where(Users.id == id).values(**fields).returning(Users)
        user = self.session.scalar(stmt)
        return user

