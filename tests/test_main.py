from fastapi import FastAPI
from fastapi.testclient import TestClient
from mensapi.api.main import app

client = TestClient(app)

def test_read_main():
    # Arrange
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}
#
# def test_today():
#     # Arrange
#     response = client.get("api/today")
#     assert response.json() = {
#
#
#         # I want to mock today to always point toward the same day
#         # Then write up the json that is supposed to be returned
#         # Then test
#
#
#
#     }
