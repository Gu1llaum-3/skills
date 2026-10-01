from datetime import timedelta

import pytest

from atelier import bookings, notifications
from atelier.cli import main
from atelier.errors import Forbidden, RuleError


def make(store, in_days, day=5):
    return bookings.create_booking(store, store.get_member(1), 1, in_days(day), in_days(day, 20))


def test_ac1_author_moves_booking(store, in_days):
    b = make(store, in_days)
    moved = bookings.update_reservation(store, store.get_member(1), b.id, in_days(6), in_days(6, 21))
    assert (moved.start, moved.end) == (in_days(6), in_days(6, 21))


def test_ac1_other_association_cannot_move(store, in_days):
    b = make(store, in_days)
    with pytest.raises(Forbidden):
        bookings.update_reservation(store, store.get_member(4), b.id, in_days(6), in_days(6, 21))


def test_ac1_refuses_less_than_24_hours_before(store, in_days):
    b = make(store, in_days)
    store.db.execute("UPDATE booking SET start = ? WHERE id = ?",
                     ((in_days(0) + timedelta(hours=20)).isoformat(), b.id))
    with pytest.raises(RuleError):
        bookings.update_reservation(store, store.get_member(1), b.id, in_days(6), in_days(6, 21))


def test_ac2_moving_at_quota_does_not_count_itself(store, in_days):
    ids = [make(store, in_days, day).id for day in range(3, 9)]
    bookings.update_reservation(store, store.get_member(1), ids[0], in_days(12), in_days(12, 20))


def test_ac3_validated_booking_goes_back_to_pending_and_notifies(store, in_days):
    b = make(store, in_days)
    store.set_status(b.id, "validated")
    bookings.update_reservation(store, store.get_member(1), b.id, in_days(6), in_days(6, 21))
    assert store.get_booking(b.id).status == "pending"
    assert notifications.outbox[-1]["subject"] == "Réservation déplacée"


def test_ac4_keeps_previous_slot(store, in_days):
    b = make(store, in_days)
    bookings.update_reservation(store, store.get_member(1), b.id, in_days(6), in_days(6, 21))
    row = store.db.execute("SELECT * FROM booking WHERE id = ?", (b.id,)).fetchone()
    assert row["previous_start"] == in_days(5).isoformat()
    assert row["updated_at"] is not None


def test_ac5_cli_move(store, in_days, tmp_path):
    b = make(store, in_days)
    db = store.db.execute("PRAGMA database_list").fetchone()["file"]
    assert main(["--db", db, "--member", "1", "move", str(b.id), in_days(6).isoformat(),
                 in_days(6, 21).isoformat()]) == 0
