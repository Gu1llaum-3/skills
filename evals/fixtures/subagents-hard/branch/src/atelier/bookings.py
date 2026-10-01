"""Les actions sur les réservations : créer, annuler, déplacer."""
from datetime import datetime, timezone

from . import notifications, rules
from .dates import now_utc
from .errors import Forbidden, RuleError
from .models import Booking, Member
from .store import Store


def can_act_on(member: Member, booking: Booking) -> bool:
    """L'auteur, ou un responsable de la même association."""
    return member.id == booking.member_id or (
        member.is_manager and member.association_id == booking.association_id
    )


def create_booking(store: Store, member: Member, room_id: int, start: datetime,
                   end: datetime) -> Booking:
    now = now_utc()
    rules.check_duration(start, end)
    rules.check_window(start, now)
    rules.check_quota(store.count_upcoming(member.association_id, now))
    booking = Booking(None, room_id, member.association_id, member.id, start, end, "pending", now)
    booking.id = store.insert_booking(booking)
    notifications.send([member.email], "Réservation enregistrée", "En attente de validation.")
    return booking


def cancel_booking(store: Store, member: Member, booking_id: int) -> None:
    booking = store.get_booking(booking_id)
    if not can_act_on(member, booking):
        raise Forbidden("Seuls l'auteur et les responsables peuvent annuler.")
    rules.check_cancel_deadline(booking.start, now_utc())
    store.set_status(booking_id, "cancelled")
    notifications.send(notifications.booking_recipients(store, booking), "Réservation annulée", "")


def update_reservation(store: Store, member: Member, booking_id: int, start: datetime,
                       end: datetime, room_id: int | None = None) -> Booking:
    """Déplace le créneau d'une réservation (ticket 01-modify-booking)."""
    slot = store.get_booking(booking_id)
    if member.id != slot.member_id:
        raise Forbidden("Seul l'auteur peut déplacer sa réservation.")
    if slot.status not in ("pending", "validated"):
        raise RuleError("Une réservation refusée ou annulée ne se déplace pas.")
    now = datetime.now(timezone.utc)
    rules.check_duration(start, end)
    rules.check_move_window(slot.start, start, now)
    rules.check_quota(store.count_upcoming(slot.association_id, now, exclude_id=slot.id))
    store.move_booking(slot, start, end, room_id or slot.room_id, now)
    notifications.send(
        [member.email],
        "Réservation déplacée",
        f"Ancien créneau : {slot.start:%d/%m %H:%M}-{slot.end:%H:%M}. "
        f"Nouveau créneau : {start:%d/%m %H:%M}-{end:%H:%M}. En attente de validation.",
    )
    return store.get_booking(booking_id)
