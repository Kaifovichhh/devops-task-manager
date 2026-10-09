# Backlog

## Done (Sprint 1)
- [x] US-1 Create task
- [x] US-2 List and filter tasks by status
- [x] US-3 Update / complete task
- [x] US-4 Delete task
- [x] US-5 Health check endpoint
- [x] US-6 Persistent storage (SQLite + Docker volume)
- [x] US-7 Automated tests in CI
- [x] US-8 One-command run with Docker Compose

## Future enhancements
- [ ] User authentication (JWT) and task assignees
- [ ] Migrate SQLite → PostgreSQL as a second service in docker-compose
- [ ] Due dates and overdue notifications
- [ ] Push the image to Docker Hub / GitHub Container Registry from CI on tag `v*`
- [ ] Automatic deploy (CD) to a cloud VM / Render / Railway
- [ ] Monitoring: Prometheus metrics endpoint + Grafana dashboard
- [ ] Simple web UI (HTML/JS) on top of the API
- [ ] Kubernetes manifests (Deployment, Service)
