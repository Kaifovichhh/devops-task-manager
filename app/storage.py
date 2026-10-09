"""SQLite storage layer for tasks.

Owner: Danas (QA / Database). Branch: feature/storage-tests
"""
import sqlite3
from datetime import datetime, timezone

VALID_STATUSES = ("todo", "in_progress", "done")
VALID_PRIORITIES = ("low", "medium", "high")

SCHEMA = """
CREATE TABLE IF NOT EXISTS tasks (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    title       TEXT    NOT NULL,
    description TEXT    NOT NULL DEFAULT '',
    status      TEXT    NOT NULL DEFAULT 'todo',
    priority    TEXT    NOT NULL DEFAULT 'medium',
    created_at  TEXT    NOT NULL,
    updated_at  TEXT    NOT NULL
);
"""


def _now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


class TaskStorage:
    """Small repository class: every method opens a short-lived connection."""

    def __init__(self, db_path):
        self.db_path = db_path
        with self._connect() as conn:
            conn.executescript(SCHEMA)

    def _connect(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def create(self, title, description="", priority="medium"):
        now = _now()
        with self._connect() as conn:
            cur = conn.execute(
                "INSERT INTO tasks (title, description, status, priority, created_at, updated_at)"
                " VALUES (?, ?, 'todo', ?, ?, ?)",
                (title, description, priority, now, now),
            )
            task_id = cur.lastrowid
        return self.get(task_id)

    def get(self, task_id):
        with self._connect() as conn:
            row = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
        return dict(row) if row else None

    def list(self, status=None):
        query = "SELECT * FROM tasks"
        params = ()
        if status:
            query += " WHERE status = ?"
            params = (status,)
        query += " ORDER BY id"
        with self._connect() as conn:
            rows = conn.execute(query, params).fetchall()
        return [dict(r) for r in rows]

    def update(self, task_id, **fields):
        allowed = {k: v for k, v in fields.items()
                   if k in ("title", "description", "status", "priority")}
        if not allowed:
            return self.get(task_id)
        allowed["updated_at"] = _now()
        assignments = ", ".join(f"{k} = ?" for k in allowed)
        with self._connect() as conn:
            cur = conn.execute(
                f"UPDATE tasks SET {assignments} WHERE id = ?",
                (*allowed.values(), task_id),
            )
            if cur.rowcount == 0:
                return None
        return self.get(task_id)

    def delete(self, task_id):
        with self._connect() as conn:
            cur = conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        return cur.rowcount > 0

    def stats(self):
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT status, COUNT(*) AS n FROM tasks GROUP BY status"
            ).fetchall()
        counts = {s: 0 for s in VALID_STATUSES}
        counts.update({r["status"]: r["n"] for r in rows})
        counts["total"] = sum(counts[s] for s in VALID_STATUSES)
        return counts

    def ping(self):
        with self._connect() as conn:
            conn.execute("SELECT 1")
        return True
