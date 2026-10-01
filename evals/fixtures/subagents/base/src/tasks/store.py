import json
import logging
from pathlib import Path

from .dates import iso, parse
from .errors import StoreError
from .model import Task

log = logging.getLogger(__name__)


class Store:
    """Les tâches, rangées dans un fichier JSON."""

    def __init__(self, path: Path):
        self.path = path

    def load(self) -> list[Task]:
        if not self.path.exists():
            return []
        try:
            raw = json.loads(self.path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise StoreError(f"Fichier de tâches illisible : {self.path}") from exc
        return [
            Task(
                id=t["id"],
                title=t["title"],
                done=t["done"],
                due=parse(t["due"]) if t.get("due") else None,
                tags=t.get("tags", []),
            )
            for t in raw
        ]

    def save(self, tasks: list[Task]) -> None:
        data = [
            {
                "id": t.id,
                "title": t.title,
                "done": t.done,
                "due": iso(t.due) if t.due else None,
                "tags": t.tags,
            }
            for t in tasks
        ]
        self.path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        log.debug("%d tâches enregistrées", len(tasks))

    def add(self, title: str) -> Task:
        tasks = self.load()
        task = Task(id=max((t.id for t in tasks), default=0) + 1, title=title)
        tasks.append(task)
        self.save(tasks)
        return task
