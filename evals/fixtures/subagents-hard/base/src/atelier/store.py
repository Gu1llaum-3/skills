import sqlite3
import sys
from contextlib import contextmanager
from pathlib import Path

from .dates import from_text, to_text
from .errors import NotFound
from .models import Booking, Member

MIGRATIONS = Path(__file__).resolve().parents[2] / "migrations"


class Store:
    def __init__(self, path: str):
        self.db = sqlite3.connect(path, isolation_level=None)
        self.db.row_factory = sqlite3.Row

    def migrate(self) -> None:
        for sql in sorted(MIGRATIONS.glob("*.sql")):
            self.db.executescript(sql.read_text(encoding="utf-8"))

    @contextmanager
    def transaction(self):
        self.db.execute("BEGIN IMMEDIATE")
        try:
            yield self.db
        except BaseException:
            self.db.execute("ROLLBACK")
            raise
        self.db.execute("COMMIT")

    def get_member(self, member_id: int) -> Member:
        row = self.db.execute("SELECT * FROM member WHERE id = ?", (member_id,)).fetchone()
        if row is None:
            raise NotFound(f"Membre {member_id} introuvable.")
        return Member(row["id"], row["association_id"], row["email"], row["role"])

    def managers_of(self, association_id: int) -> list[Member]:
        rows = self.db.execute(
            "SELECT * FROM member WHERE association_id = ? AND role = 'manager'", (association_id,)
        ).fetchall()
        return [Member(r["id"], r["association_id"], r["email"], r["role"]) for r in rows]

    def get_booking(self, booking_id: int) -> Booking:
        row = self.db.execute("SELECT * FROM booking WHERE id = ?", (booking_id,)).fetchone()
        if row is None:
            raise NotFound(f"Réservation {booking_id} introuvable.")
        return _booking(row)

    def count_upcoming(self, association_id: int, now) -> int:
        return self.db.execute(
            "SELECT COUNT(*) FROM booking WHERE association_id = ? AND start > ?"
            " AND status IN ('pending', 'validated')",
            (association_id, to_text(now)),
        ).fetchone()[0]

    def insert_booking(self, b: Booking) -> int:
        with self.transaction() as db:
            cur = db.execute(
                "INSERT INTO booking (room_id, association_id, member_id, start, end, status,"
                " created_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (b.room_id, b.association_id, b.member_id, to_text(b.start), to_text(b.end),
                 b.status, to_text(b.created_at)),
            )
            return cur.lastrowid

    def set_status(self, booking_id: int, status: str) -> None:
        with self.transaction() as db:
            db.execute("UPDATE booking SET status = ? WHERE id = ?", (status, booking_id))


def _booking(row) -> Booking:
    return Booking(row["id"], row["room_id"], row["association_id"], row["member_id"],
                   from_text(row["start"]), from_text(row["end"]), row["status"],
                   from_text(row["created_at"]))


if __name__ == "__main__" and sys.argv[1:2] == ["--init"]:
    Store(sys.argv[2]).migrate()
