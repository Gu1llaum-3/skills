from datetime import date


def iso(value: date) -> str:
    """Date au format ISO 8601 (AAAA-MM-JJ). Lève TypeError si value n'est pas une date."""
    if not isinstance(value, date):
        raise TypeError(f"date attendue, reçu {type(value).__name__}")
    return value.isoformat()


def parse(text: str) -> date:
    return date.fromisoformat(text)
