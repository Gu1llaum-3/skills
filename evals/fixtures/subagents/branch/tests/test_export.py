from datetime import date

from tasks.cli import main
from tasks.export import to_csv
from tasks.model import Task
from tasks.store import Store


def test_ac1_header_and_one_line_per_task_with_oui_non(tmp_path):
    target = tmp_path / "out.csv"
    to_csv([Task(id=1, title="A", done=True), Task(id=2, title="B")], target)
    assert target.read_text(encoding="utf-8").splitlines() == [
        "id,title,done,due",
        "1,A,oui,",
        "2,B,non,",
    ]


def test_ac2_done_flag_keeps_only_finished_tasks(tmp_path):
    Store(tmp_path / "tasks.json").save(
        [Task(id=1, title="A", done=True), Task(id=2, title="B", due=date(2026, 1, 5))]
    )
    target = tmp_path / "out.csv"
    assert main(["--file", str(tmp_path / "tasks.json"), "export", str(target), "--done"]) == 0
    assert len(target.read_text(encoding="utf-8").splitlines()) == 2
