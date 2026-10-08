# ---------- Stage 1: run tests inside the build (fails the build if tests fail) ----------
FROM python:3.12-slim AS test
WORKDIR /src
COPY requirements.txt requirements-dev.txt ./
RUN pip install --no-cache-dir -r requirements-dev.txt
COPY . .
RUN flake8 app tests wsgi.py && pytest -q

# ---------- Stage 2: small production image ----------
FROM python:3.12-slim AS runtime
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DATABASE_PATH=/data/tasks.db \
    PORT=5000
WORKDIR /app

# Non-root user for security
RUN useradd --create-home --uid 1000 appuser && mkdir -p /data && chown appuser /data

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app ./app
COPY wsgi.py .

USER appuser
EXPOSE 5000
VOLUME ["/data"]

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD python -c "import urllib.request,sys; sys.exit(0 if urllib.request.urlopen('http://localhost:5000/health').status==200 else 1)"

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "wsgi:app"]
