from .users_model import Users
from ..core.database import Base, engine

Base.metadata.create_all(bind=engine)

