# Task Manager API — DevOps Team Project

![CI](https://github.com/Kaifovichhh/devops-task-manager/actions/workflows/ci.yml/badge.svg)

A small REST API for managing team tasks (create, list, filter, update, delete, statistics).
The goal of the project is **not** the business logic itself but the full DevOps lifecycle around it:
Git branching, automated tests, Docker containerisation and a CI pipeline on GitHub Actions.

| | |
|---|---|
| Language | Python 3.12 (works on 3.9+) |
| Framework | Flask 3 + Gunicorn |
| Database | SQLite (stored in a Docker volume) |
| Tests | pytest + pytest-cov (17 tests, ~97 % coverage) |
| Lint | flake8 |
| Container | Docker (multi-stage) + Docker Compose |
| CI | GitHub Actions (`.github/workflows/ci.yml`) |

## Team

| Member | Role | Branch | Owns |
|---|---|---|---|
| Student 1 | Team Lead / Backend developer | `feature/tasks-api` | `app/routes.py`, `app/__init__.py` |
| Student 2 | QA engineer / Database | `feature/storage-tests` | `app/storage.py`, `tests/` |
| Student 3 | DevOps engineer | `feature/docker-ci` | `Dockerfile`, `docker-compose.yml`, `.github/workflows/ci.yml` |

## Quick start

### Option A — Docker (recommended)

```bash
docker compose up --build -d
curl http://localhost:5000/health
```

Data is kept in the named volume `task-data`, so tasks survive `docker compose down` / `up`.
Use `docker compose down -v` to wipe the data.

### Option B — local Python

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
python wsgi.py              # http://localhost:5000
```

### Run the tests

```bash
flake8 app tests wsgi.py
pytest -v --cov=app
```

## API

| Method | Endpoint | Description | Success |
|---|---|---|---|
| GET | `/health` | Service + DB health (used by Docker HEALTHCHECK) | 200 |
| GET | `/tasks` | List tasks, optional `?status=todo\|in_progress\|done` | 200 |
| POST | `/tasks` | Create task `{"title", "description"?, "priority"?}` | 201 |
| GET | `/tasks/<id>` | Get one task | 200 / 404 |
| PATCH | `/tasks/<id>` | Update `title`, `description`, `status`, `priority` | 200 / 400 / 404 |
| DELETE | `/tasks/<id>` | Delete task | 204 / 404 |
| GET | `/stats` | Number of tasks per status | 200 |

Example:

```bash
curl -X POST http://localhost:5000/tasks -H "Content-Type: application/json" \
     -d '{"title":"Prepare slides","priority":"high"}'
curl -X PATCH http://localhost:5000/tasks/1 -H "Content-Type: application/json" \
     -d '{"status":"done"}'
curl http://localhost:5000/tasks?status=done
```

## Project structure

```
app/
  __init__.py        application factory (create_app)
  routes.py          REST endpoints + input validation
  storage.py         SQLite repository
tests/
  test_api.py        API tests TC-01..TC-12
  test_storage.py    storage tests TC-13..TC-15
wsgi.py              entry point (dev server / gunicorn)
Dockerfile           multi-stage: test stage -> runtime stage
docker-compose.yml   one service + persistent volume
.github/workflows/ci.yml   lint -> tests -> docker build -> smoke test
docs/                Git workflow, test cases, backlog
```

## How to continue the project

1. Read [docs/GIT_WORKFLOW.md](docs/GIT_WORKFLOW.md) — branch from `develop`, open a Pull Request.
2. Pick an item from [docs/BACKLOG.md](docs/BACKLOG.md).
3. Add tests for every new feature in `tests/` (see [docs/TEST_CASES.md](docs/TEST_CASES.md)).
4. CI must be green before merging.

**Repository:** https://github.com/Kaifovichhh/devops-task-manager
