"""API tests (TC-01 ... TC-12). Owner: Student 1 + Student 2."""


def _create(client, **kwargs):
    payload = {"title": "Write Dockerfile", **kwargs}
    return client.post("/tasks", json=payload)


# TC-01: health check used by Docker HEALTHCHECK and CI smoke test
def test_health_ok(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.get_json()["status"] == "ok"


# TC-02: create a task with defaults
def test_create_task(client):
    resp = _create(client, description="multi-stage build")
    assert resp.status_code == 201
    body = resp.get_json()
    assert body["id"] == 1
    assert body["status"] == "todo"
    assert body["priority"] == "medium"


# TC-03: title is required
def test_create_task_without_title_returns_400(client):
    resp = client.post("/tasks", json={"description": "no title"})
    assert resp.status_code == 400
    assert "title" in resp.get_json()["error"]


# TC-04: blank title / non-JSON body rejected
def test_create_task_invalid_payloads(client):
    assert client.post("/tasks", json={"title": "   "}).status_code == 400
    assert client.post("/tasks", data="not json").status_code == 400
    assert client.post("/tasks", json={"title": "x" * 201}).status_code == 400


# TC-05: invalid priority rejected
def test_create_task_invalid_priority(client):
    assert _create(client, priority="urgent").status_code == 400


# TC-06: list tasks
def test_list_tasks(client):
    _create(client, title="A")
    _create(client, title="B")
    resp = client.get("/tasks")
    assert resp.status_code == 200
    assert [t["title"] for t in resp.get_json()] == ["A", "B"]


# TC-07: filter by status
def test_filter_tasks_by_status(client):
    _create(client, title="A")
    _create(client, title="B")
    client.patch("/tasks/2", json={"status": "done"})
    done = client.get("/tasks?status=done").get_json()
    assert [t["title"] for t in done] == ["B"]
    assert client.get("/tasks?status=unknown").status_code == 400


# TC-08: get a single task / 404
def test_get_task(client):
    _create(client)
    assert client.get("/tasks/1").get_json()["title"] == "Write Dockerfile"
    assert client.get("/tasks/999").status_code == 404


# TC-09: update status (mark as done)
def test_update_task_status(client):
    _create(client)
    resp = client.patch("/tasks/1", json={"status": "done", "priority": "high"})
    assert resp.status_code == 200
    body = resp.get_json()
    assert body["status"] == "done"
    assert body["priority"] == "high"


# TC-10: update validation and missing task
def test_update_task_errors(client):
    _create(client)
    assert client.patch("/tasks/1", json={"status": "finished"}).status_code == 400
    assert client.patch("/tasks/1", json={"title": ""}).status_code == 400
    assert client.patch("/tasks/42", json={"status": "done"}).status_code == 404


# TC-11: delete a task
def test_delete_task(client):
    _create(client)
    assert client.delete("/tasks/1").status_code == 204
    assert client.get("/tasks/1").status_code == 404
    assert client.delete("/tasks/1").status_code == 404


# TC-12: statistics endpoint
def test_stats(client):
    _create(client, title="A")
    _create(client, title="B")
    client.patch("/tasks/1", json={"status": "in_progress"})
    stats = client.get("/stats").get_json()
    assert stats == {"todo": 1, "in_progress": 1, "done": 0, "total": 2}


def test_unknown_route_returns_json_404(client):
    resp = client.get("/nope")
    assert resp.status_code == 404
    assert resp.get_json() == {"error": "Not found"}
