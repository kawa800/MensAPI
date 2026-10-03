from fastapi import FastAPI
import datetime as dt

from mensapi.api.main import app


def test_read_main(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Oliebe"}


def test_week_start_after_end_date(client):
    response = client.get("/api/week/?start=2026-09-24&end=2026-09-21")
    assert response.status_code == 400
    assert response.json() == {"detail":"The query parameter 'start' must be before or equal to 'end'."}


def test_today_weekend(client, today_dishes, set_date):
    set_date(dt.date(2026, 10, 3)) # Saturday
    response = client.get("/api/today")
    assert response.status_code == 200
    assert response.json() == {"detail": "There are no dishes on the weekend."}


def test_week_current(client, db_current_dish_oli):
    """ 
    When a database sets the time as now and the dish as 'Orientalischer Linseneintopf',
    then the endpoint '/api/week/current returns the data of this dish
    """
    response = client.get("/api/week/current")
    assert response.status_code == 200
    assert response.json()[0]["name"] == db_current_dish_oli.name
