from datetime import timedelta

import pytest

from atelier import notifications
from atelier.dates import now_utc
from atelier.store import Store


@pytest.fixture
def store(tmp_path):
    s = Store(str(tmp_path / "test.db"))
    s.migrate()
    s.db.executescript("""
        INSERT INTO association (id, name) VALUES (1, 'Chorale'), (2, 'Échecs');
        INSERT INTO member (id, association_id, email, role) VALUES
            (1, 1, 'auteur@chorale.fr', 'member'),
            (2, 1, 'resp@chorale.fr', 'manager'),
            (3, 1, 'autre@chorale.fr', 'member'),
            (4, 2, 'resp@echecs.fr', 'manager');
        INSERT INTO room (id, name, capacity) VALUES (1, 'Grande salle', 80), (2, 'Atelier', 15);
    """)
    notifications.outbox.clear()
    return s


@pytest.fixture
def in_days():
    """Une heure pile, dans n jours, en UTC."""
    def make(days, hour=18):
        return (now_utc() + timedelta(days=days)).replace(hour=hour, minute=0, second=0,
                                                         microsecond=0)
    return make
