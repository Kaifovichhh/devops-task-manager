import pytest

from app import create_app
from app.storage import TaskStorage


@pytest.fixture
def app(tmp_path):
    return create_app({"DATABASE": str(tmp_path / "test.db"), "TESTING": True})


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def storage(tmp_path):
    return TaskStorage(str(tmp_path / "storage.db"))
