# Git workflow

We use a simplified **Git Flow**:

```
main ────●──────────────────────────────●──── (stable, tagged releases: v1.0.0)
          \                            /
develop    ●──────●───────●───────●───●       (integration branch)
            \    /       /       /
feature/tasks-api       /       /             Student 1
             feature/storage-tests            Student 2
                         feature/docker-ci    Student 3
```

## Branches

| Branch | Purpose | Who can merge |
|---|---|---|
| `main` | Production-ready code. Protected: no direct pushes, PR + green CI + 1 review required. | Team Lead |
| `develop` | Integration of finished features. | Any member via PR |
| `feature/<name>` | One feature per branch, created from `develop`. | Owner opens PR into `develop` |

## How the master (main) branch was created

```bash
git init
git checkout -b main
git add README.md .gitignore requirements.txt
git commit -m "chore: initial project skeleton"
git remote add origin https://github.com/Kaifovichhh/devops-task-manager.git
git push -u origin main
```

Then on GitHub: **Settings → Branches → Add rule for `main`**:
require pull request, require status check `Lint & Test`, block force pushes.

## How a personal branch is created

```bash
git checkout develop
git pull
git checkout -b feature/docker-ci
# ... work, commit often ...
git add Dockerfile docker-compose.yml
git commit -m "feat(docker): multi-stage Dockerfile with healthcheck"
git push -u origin feature/docker-ci
# open Pull Request feature/docker-ci -> develop on GitHub
```

## Commit message convention

`<type>(<scope>): <summary>` — types: `feat`, `fix`, `test`, `docs`, `ci`, `chore`, `refactor`.
