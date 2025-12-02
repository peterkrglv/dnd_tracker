from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient

_mongo_patcher = patch("pymongo.MongoClient", MagicMock())
_mongo_patcher.start()

from main import app


@pytest.fixture(scope="session", autouse=True)
def _stop_mongo_patcher():
    yield
    _mongo_patcher.stop()


@pytest.fixture
def client():
    return TestClient(app)
