from datetime import datetime, timezone


def now_utc() -> datetime:
    return datetime.now(timezone.utc)


def to_text(value: datetime) -> str:
    if value.tzinfo is None:
        raise ValueError("datetime sans fuseau")
    return value.astimezone(timezone.utc).isoformat()


def from_text(text: str) -> datetime:
    return datetime.fromisoformat(text)
