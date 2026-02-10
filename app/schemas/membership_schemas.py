from pydantic import BaseModel
from datetime import datetime
from ..models import ProjectRole

class MembershipBase(BaseModel):
    role: ProjectRole

class Membership(MembershipBase):
    id: int
    is_invited: bool
    invited_at: datetime
    invited_by: int
    user_id: int
    project_id: int
