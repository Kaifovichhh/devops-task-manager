"""REST API endpoints.

Owner: Student 1 (Team Lead / Backend). Branch: feature/tasks-api
"""
from flask import Blueprint, current_app, jsonify, request

from .storage import VALID_PRIORITIES, VALID_STATUSES

api = Blueprint("api", __name__)


def _storage():
    return current_app.config["STORAGE"]


def _error(message, code):
    return jsonify({"error": message}), code


def _validate(data, partial=False):
    """Return an error message, or None if the payload is valid."""
    if not isinstance(data, dict):
        return "Request body must be a JSON object"
    if not partial or "title" in data:
        title = data.get("title")
        if not isinstance(title, str) or not title.strip():
            return "Field 'title' is required and must be a non-empty string"
        if len(title) > 200:
            return "Field 'title' must be at most 200 characters"
    if "status" in data and data["status"] not in VALID_STATUSES:
        return f"Field 'status' must be one of {list(VALID_STATUSES)}"
    if "priority" in data and data["priority"] not in VALID_PRIORITIES:
        return f"Field 'priority' must be one of {list(VALID_PRIORITIES)}"
    if "description" in data and not isinstance(data["description"], str):
        return "Field 'description' must be a string"
    return None


@api.get("/health")
def health():
    try:
        _storage().ping()
        return jsonify({"status": "ok", "database": "ok",
                        "version": current_app.config["APP_VERSION"]})
    except Exception:  # pragma: no cover - only when the DB file is broken
        return jsonify({"status": "error", "database": "unavailable"}), 503


@api.get("/tasks")
def list_tasks():
    status = request.args.get("status")
    if status and status not in VALID_STATUSES:
        return _error(f"Query 'status' must be one of {list(VALID_STATUSES)}", 400)
    return jsonify(_storage().list(status=status))


@api.post("/tasks")
def create_task():
    data = request.get_json(silent=True)
    err = _validate(data)
    if err:
        return _error(err, 400)
    task = _storage().create(
        title=data["title"].strip(),
        description=data.get("description", ""),
        priority=data.get("priority", "medium"),
    )
    return jsonify(task), 201


@api.get("/tasks/<int:task_id>")
def get_task(task_id):
    task = _storage().get(task_id)
    if task is None:
        return _error("Task not found", 404)
    return jsonify(task)


@api.patch("/tasks/<int:task_id>")
def update_task(task_id):
    data = request.get_json(silent=True)
    err = _validate(data, partial=True)
    if err:
        return _error(err, 400)
    if "title" in data:
        data["title"] = data["title"].strip()
    task = _storage().update(task_id, **data)
    if task is None:
        return _error("Task not found", 404)
    return jsonify(task)


@api.delete("/tasks/<int:task_id>")
def delete_task(task_id):
    if not _storage().delete(task_id):
        return _error("Task not found", 404)
    return "", 204


@api.get("/stats")
def stats():
    return jsonify(_storage().stats())
