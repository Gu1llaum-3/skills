import csv
import json
from pathlib import Path

from .model import Task


class ExportError(Exception):
    pass


def to_csv(tasks: list[Task], path: Path, force: bool = False) -> int:
    """Écrit les tâches dans un CSV et renvoie le nombre de lignes écrites."""
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "title", "done", "due"])
        for t in tasks:
            due = t.due.strftime("%d/%m/%Y") if t.due else ""
            writer.writerow([t.id, t.title, "oui" if t.done else "non", due])
    print(f"{len(tasks)} tâches exportées vers {path}")
    return len(tasks)


def to_json(tasks: list[Task], path: Path) -> int:
    data = [{"id": t.id, "title": t.title, "done": t.done} for t in tasks]
    path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    return len(tasks)
