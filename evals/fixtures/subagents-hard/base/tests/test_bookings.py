from datetime import timedelta

import pytest

from atelier import bookings, notifications
from atelier.errors import Forbidden, RuleError


def test_create_is_pending_and_notifies_author(store, in_days):
    b = bookings.create_booking(store, store.get_member(1), 1, in_days(5), in_days(5, 20))
    assert store.get_booking(b.id).status == "pending"
    assert notifications.outbox[-1]["to"] == ["auteur@chorale.fr"]


def test_create_refuses_less_than_48_hours_ahead(store, in_days):
    with pytest.raises(RuleError):
        bookings.create_booking(store, store.get_member(1), 1, in_days(1), in_days(1, 20))


def test_create_refuses_seventh_upcoming_booking(store, in_days):
    for day in range(3, 9):
        bookings.create_booking(store, store.get_member(1), 1, in_days(day), in_days(day, 20))
    with pytest.raises(RuleError):
        bookings.create_booking(store, store.get_member(1), 1, in_days(10), in_days(10, 20))


def test_manager_cancels_booking_of_own_association(store, in_days):
    b = bookings.create_booking(store, store.get_member(1), 1, in_days(5), in_days(5, 20))
    bookings.cancel_booking(store, store.get_member(2), b.id)
    assert store.get_booking(b.id).status == "cancelled"
    assert notifications.outbox[-1]["to"] == ["auteur@chorale.fr", "resp@chorale.fr"]


def test_other_association_cannot_cancel(store, in_days):
    b = bookings.create_booking(store, store.get_member(1), 1, in_days(5), in_days(5, 20))
    with pytest.raises(Forbidden):
        bookings.cancel_booking(store, store.get_member(4), b.id)
