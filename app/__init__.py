"""Task Manager API - application factory."""
import os

from flask import Flask, jsonify

from .routes import api
from .storage import TaskStorage

__version__ = "1.0.0"


def create_app(config=None):
    app = Flask(__name__)
    app.config.update(
        DATABASE=os.environ.get("DATABASE_PATH", "tasks.db"),
        APP_VERSION=os.environ.get("APP_VERSION", __version__),
    )
    if config:
        app.config.update(config)

    db_dir = os.path.dirname(app.config["DATABASE"])
    if db_dir:
        os.makedirs(db_dir, exist_ok=True)
    app.config["STORAGE"] = TaskStorage(app.config["DATABASE"])

    app.register_blueprint(api)

    @app.errorhandler(404)
    def not_found(_):
        return jsonify({"error": "Not found"}), 404

    @app.errorhandler(405)
    def method_not_allowed(_):
        return jsonify({"error": "Method not allowed"}), 405

    return app
