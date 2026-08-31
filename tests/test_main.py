from fastapi import FastAPI
from fastapi.testclient import TestClient
from mensapi.main import app

client = TestClient(app)


def test_read_main():
    # Arrange
    response = client.get("/")

    # Act
    json = response.json()

    # Assert
    assert response.status_code == 200
    assert  json == {"message": "Hello World"}


