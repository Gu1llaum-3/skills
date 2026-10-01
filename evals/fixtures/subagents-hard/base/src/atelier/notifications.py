import logging

from .models import Booking
from .store import Store

log = logging.getLogger(__name__)
outbox: list[dict] = []  # remplacé par l'envoi SMTP en production


def send(to: list[str], subject: str, body: str) -> None:
    outbox.append({"to": to, "subject": subject, "body": body})
    log.info("courriel « %s » pour %d destinataires", subject, len(to))


def booking_recipients(store: Store, booking: Booking) -> list[str]:
    """L'auteur de la réservation et les responsables de son association, sans doublon."""
    emails = [store.get_member(booking.member_id).email]
    emails += [m.email for m in store.managers_of(booking.association_id)]
    return list(dict.fromkeys(emails))
