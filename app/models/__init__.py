from ..core.database import Base, engine

from .users_model import Users
from .project_model import Projects
from .membership_model import Memberships, ProjectRole

Base.metadata.create_all(bind=engine)
