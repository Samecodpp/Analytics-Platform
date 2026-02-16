from sqlalchemy import update, select, insert

from ..models import Users
from .base_repo import BaseRepository


class UserRepository(BaseRepository):
    def get_by_id(self, id: int) -> Users | None:
        return self.session.get(Users, id)

    def get_by_email(self, email: str) -> Users | None:
        stmt = select(Users).where(Users.email == email)
        user = self.session.scalar(stmt)
        return user

    def create(self, fields: dict) -> Users | None:
        stmt = insert(Users).values(**fields).returning(Users)
        new_user = self.session.scalar(stmt)
        return new_user

    def update_by_id(self, id: int, fields: dict) -> Users | None:
        stmt = update(Users).where(Users.id == id).values(**fields).returning(Users)
        user = self.session.scalar(stmt)
        return user
