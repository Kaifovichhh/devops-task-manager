"""Entry point: `python wsgi.py` for development, `gunicorn wsgi:app` in Docker."""
import os

from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
