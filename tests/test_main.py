from fastapi import FastAPI
from fastapi.testclient import TestClient

from mensapi.api.main import app
from tests.conftest import TestingSessionLocal

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Oliebe"}


def test_week_start_after_end_date():
    response = client.get("/api/week/?start=2026-09-24&end=2026-09-21")
    assert response.status_code == 400
    assert response.json() == {"detail":"The query parameter 'start' must be before or equal to 'end'."}


# Gives a certain menu in the fake database
def test_week_current():
    response = client.get("/api/week/current")
    assert response.status_code == 200
    assert response.json() == {"detail":"The query parameter 'start' must be before or equal to 'end'."}
