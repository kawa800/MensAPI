from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import sessionmaker

from mensapi.api.main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Oliebe"}


def test_week_start_after_end_date():
    response = client.get("/api/week/?start=2026-09-24&end=2026-09-21")
    assert response.status_code == 400
    assert response.json() == {"detail":"The query parameter 'start' must be before or equal to 'end'."}


def test_week_current():
    response = client.get("/api/week/current")
    assert response.status_code == 200
    assert response.json() == {"detail":"The query parameter 'start' must be before or equal to 'end'."}
