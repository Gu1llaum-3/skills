from dataclasses import dataclass
from datetime import datetime


@dataclass
class Member:
    id: int
    association_id: int
    email: str
    role: str  # "member" ou "manager"

    @property
    def is_manager(self) -> bool:
        return self.role == "manager"


@dataclass
class Booking:
    id: int | None
    room_id: int
    association_id: int
    member_id: int
    start: datetime
    end: datetime
    status: str
    created_at: datetime
