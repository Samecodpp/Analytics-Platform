from dataclasses import dataclass
from .base_event import BaseEvent

@dataclass
class RegisterEvent(BaseEvent):
    user_id: str
    email: str
    username: str

    def __post_init__(self):
        self.event_name = "auth.user_registered"
