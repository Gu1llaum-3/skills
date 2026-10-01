"""Règles métier des réservations. Chaque fonction lève RuleError si la règle n'est pas tenue."""
from datetime import datetime, timedelta

from .errors import RuleError

MIN_DURATION = timedelta(hours=1)
MAX_DURATION = timedelta(hours=8)
MIN_NOTICE = timedelta(hours=48)
MAX_ADVANCE = timedelta(days=60)
CANCEL_DEADLINE = timedelta(hours=24)
MAX_UPCOMING = 6
OPENING_HOUR, CLOSING_HOUR = 8, 23


def check_duration(start: datetime, end: datetime) -> None:
    if end <= start:
        raise RuleError("La fin doit suivre le début.")
    if not MIN_DURATION <= end - start <= MAX_DURATION:
        raise RuleError("Une réservation dure entre 1 et 8 heures.")
    if start.minute % 30 or end.minute % 30:
        raise RuleError("Les créneaux se prennent par demi-heure.")


def check_window(start: datetime, now: datetime) -> None:
    """Création : au plus tôt 60 jours avant, au plus tard 48 heures avant le début."""
    if start - now < MIN_NOTICE:
        raise RuleError("On réserve au plus tard 48 heures avant le début.")
    if start - now > MAX_ADVANCE:
        raise RuleError("On réserve au plus tôt 60 jours à l'avance.")


def check_quota(upcoming: int) -> None:
    """upcoming : réservations à venir de l'association, hors refusées et annulées."""
    if upcoming >= MAX_UPCOMING:
        raise RuleError("Votre association a déjà 6 réservations à venir.")


def check_cancel_deadline(start: datetime, now: datetime) -> None:
    if start - now < CANCEL_DEADLINE:
        raise RuleError("Moins de 24 heures avant le début : l'annulation passe par un agent.")


def check_move_window(old_start: datetime, new_start: datetime, now: datetime) -> None:
    """Déplacement : 24 heures avant le créneau actuel et le nouveau, 60 jours au plus."""
    if old_start - now < CANCEL_DEADLINE or new_start - now < CANCEL_DEADLINE:
        raise RuleError("Moins de 24 heures avant le début : le déplacement passe par un agent.")
    if new_start - now > MAX_ADVANCE:
        raise RuleError("On réserve au plus tôt 60 jours à l'avance.")
