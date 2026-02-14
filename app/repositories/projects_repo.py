from typing import List
from sqlalchemy import insert, select

from ..models import Memberships, ProjectRole
from .base_repo import BaseRepository
from ..models import Projects

class ProjectRepository(BaseRepository):
    def create(self, fields: dict) -> Projects | None:
        stmt = insert(Projects).values(**fields).returning(Projects)
        new_project = self.session.scalar(stmt)
        self.session.flush()
        return new_project

    def get_by_user_id(self,
                       user_id: int,
                       project_name: str | None = None,
                       role: str | None = None) -> List[Projects]:
        stmt = select(Projects).join(Memberships).where(Memberships.user_id == user_id)
        if project_name:
            stmt = stmt.where(Projects.name == project_name)
        if role:
            stmt = stmt.where(Memberships.role == role)

        projects = self.session.scalars(stmt).all()
        return list(projects)



