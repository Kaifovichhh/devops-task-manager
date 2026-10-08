"""Storage layer unit tests (TC-13 ... TC-15). Owner: Student 2."""
from app.storage import TaskStorage


# TC-13: data survives re-opening the database (simulates container restart)
def test_persistence_between_instances(tmp_path):
    path = str(tmp_path / "persist.db")
    TaskStorage(path).create("Survive restart")
    reopened = TaskStorage(path)
    assert [t["title"] for t in reopened.list()] == ["Survive restart"]


# TC-14: update ignores unknown fields and bumps updated_at
def test_update_ignores_unknown_fields(storage):
    task = storage.create("Task")
    updated = storage.update(task["id"], status="done", id=999, hacker="x")
    assert updated["id"] == task["id"]
    assert updated["status"] == "done"
    assert "hacker" not in updated


# TC-15: update / delete of missing task
def test_missing_task(storage):
    assert storage.get(1) is None
    assert storage.update(1, status="done") is None
    assert storage.delete(1) is False


def test_stats_empty(storage):
    assert storage.stats() == {"todo": 0, "in_progress": 0, "done": 0, "total": 0}
