# Test cases

Run: `pytest -v`. All cases are automated and run in CI on every push.

| ID | Feature | Steps | Expected result | Automated test |
|---|---|---|---|---|
| TC-01 | Health check | GET `/health` | 200, `status: ok` | `test_health_ok` |
| TC-02 | Create task | POST `/tasks` `{"title":"Write Dockerfile"}` | 201, id=1, status=todo, priority=medium | `test_create_task` |
| TC-03 | Validation | POST without title | 400, error mentions `title` | `test_create_task_without_title_returns_400` |
| TC-04 | Validation | blank title, non-JSON body, 201-char title | 400 | `test_create_task_invalid_payloads` |
| TC-05 | Validation | priority=`urgent` | 400 | `test_create_task_invalid_priority` |
| TC-06 | List tasks | create A, B; GET `/tasks` | 200, [A, B] | `test_list_tasks` |
| TC-07 | Filter | mark B done; GET `/tasks?status=done` | only B; unknown status → 400 | `test_filter_tasks_by_status` |
| TC-08 | Get task | GET `/tasks/1`, `/tasks/999` | 200 / 404 | `test_get_task` |
| TC-09 | Update | PATCH status=done, priority=high | 200, fields changed | `test_update_task_status` |
| TC-10 | Update errors | invalid status, empty title, missing id | 400 / 400 / 404 | `test_update_task_errors` |
| TC-11 | Delete | DELETE `/tasks/1` twice | 204, then 404 | `test_delete_task` |
| TC-12 | Statistics | 1 todo + 1 in_progress | `{todo:1, in_progress:1, done:0, total:2}` | `test_stats` |
| TC-13 | Persistence | create, reopen DB file | task still present | `test_persistence_between_instances` |
| TC-14 | Safe update | update with unknown fields | unknown fields ignored | `test_update_ignores_unknown_fields` |
| TC-15 | Missing task | get/update/delete id=1 on empty DB | None / None / False | `test_missing_task` |

## Docker / CI checks

| ID | Check | Expected result |
|---|---|---|
| TC-D1 | `docker build .` | Stage `test` runs flake8 + pytest; build fails if any test fails |
| TC-D2 | `docker compose up -d` → `docker ps` | container `task-manager-api` is `healthy` |
| TC-D3 | Create task → `docker compose down` → `up` → GET `/tasks` | task is still there (volume) |
| TC-D4 | `docker exec task-manager-api whoami` | `appuser` (not root) |
| TC-D5 | GitHub Actions on push | jobs `Lint & Test` and `Docker build & smoke test` are green |
