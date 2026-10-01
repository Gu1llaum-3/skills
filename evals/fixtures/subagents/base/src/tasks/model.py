from dataclasses import dataclass, field
from datetime import date


@dataclass
class Task:
    id: int
    title: str
    done: bool = False
    due: date | None = None
    tags: list[str] = field(default_factory=list)
