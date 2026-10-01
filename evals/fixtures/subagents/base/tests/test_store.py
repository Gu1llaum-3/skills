from datetime import date

from tasks.model import Task
from tasks.store import Store


def test_save_then_load_keeps_due_date(tmp_path):
    store = Store(tmp_path / "tasks.json")
    store.save([Task(id=1, title="Payer", due=date(2026, 3, 1))])
    assert store.load()[0].due == date(2026, 3, 1)


def test_add_numbers_after_highest_id(tmp_path):
    store = Store(tmp_path / "tasks.json")
    store.save([Task(id=4, title="A")])
    assert store.add("B").id == 5
