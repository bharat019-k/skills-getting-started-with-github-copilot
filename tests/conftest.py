import copy

import pytest
from fastapi.testclient import TestClient

from src.app import app, activities as global_activities

# snapshot of the original activities dictionary so tests can restore it
original_activities = copy.deepcopy(global_activities)


@pytest.fixture(autouse=True)
def reset_activities():
    """Restore the global `activities` dictionary before each test."""
    global_activities.clear()
    global_activities.update(copy.deepcopy(original_activities))
    yield


@pytest.fixture
def client():
    """Return a TestClient instance for the FastAPI application."""
    return TestClient(app)
