import argparse
import sys
from datetime import datetime

from . import bookings
from .store import Store


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="atelier")
    parser.add_argument("--db", default="atelier.db")
    parser.add_argument("--member", type=int, required=True)
    sub = parser.add_subparsers(dest="command", required=True)
    book = sub.add_parser("book")
    book.add_argument("room", type=int)
    book.add_argument("start", type=datetime.fromisoformat)
    book.add_argument("end", type=datetime.fromisoformat)
    cancel = sub.add_parser("cancel")
    cancel.add_argument("booking", type=int)
    move = sub.add_parser("move")
    move.add_argument("booking", type=int)
    move.add_argument("start", type=datetime.fromisoformat)
    move.add_argument("end", type=datetime.fromisoformat)
    args = parser.parse_args(argv)
    store = Store(args.db)
    try:
        member = store.get_member(args.member)
        if args.command == "book":
            b = bookings.create_booking(store, member, args.room, args.start, args.end)
            print(f"Réservation {b.id} enregistrée, en attente de validation.")
        elif args.command == "cancel":
            bookings.cancel_booking(store, member, args.booking)
            print("Réservation annulée.")
        elif args.command == "move":
            bookings.update_reservation(store, member, args.booking, args.start, args.end)
            print("Réservation déplacée, en attente de validation.")
    except Exception as exc:  # seul endroit autorisé, voir CLAUDE.md
        print(f"Erreur : {exc}", file=sys.stderr)
        return 1
    return 0
