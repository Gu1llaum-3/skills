import argparse
import sys
from pathlib import Path

from .errors import TasksError
from .export import to_csv
from .store import Store


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tasks")
    parser.add_argument("--file", type=Path, default=Path("tasks.json"))
    sub = parser.add_subparsers(dest="command", required=True)
    add = sub.add_parser("add", help="ajouter une tâche")
    add.add_argument("title")
    sub.add_parser("list", help="lister les tâches")
    export = sub.add_parser("export", help="exporter les tâches en CSV")
    export.add_argument("target", type=Path)
    export.add_argument("--done", action="store_true", help="seulement les tâches terminées")
    export.add_argument("--force", action="store_true", help="écraser le fichier s'il existe")
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
        elif args.command == "export":
            tasks = [t for t in store.load() if t.done or not args.done]
            count = to_csv(tasks, args.target, force=args.force)
            print(f"Export terminé : {count} lignes")
    except TasksError as exc:
        print(exc, file=sys.stderr)
        return 1
    return 0
