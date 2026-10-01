import argparse
import sys
from pathlib import Path

from .errors import TasksError
from .store import Store


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tasks")
    parser.add_argument("--file", type=Path, default=Path("tasks.json"))
    sub = parser.add_subparsers(dest="command", required=True)
    add = sub.add_parser("add", help="ajouter une tâche")
    add.add_argument("title")
    sub.add_parser("list", help="lister les tâches")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    store = Store(args.file)
    try:
        if args.command == "add":
            task = store.add(args.title)
            print(f"Tâche {task.id} ajoutée")
        elif args.command == "list":
            for t in store.load():
                print(f"[{'x' if t.done else ' '}] {t.id} {t.title}")
    except TasksError as exc:
        print(exc, file=sys.stderr)
        return 1
    return 0
