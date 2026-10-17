import pytest
from fastapi.testclient import TestClient

from src.app import activities, app


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def activity(monkeypatch):
    name = "Test Activity"
    details = {
        "description": "An activity used by API tests",
        "schedule": "Mondays at 3:00 PM",
        "max_participants": 10,
        "participants": ["registered@example.com"],
    }
    monkeypatch.setitem(activities, name, details)
    return name, details