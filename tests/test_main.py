from fastapi import FastAPI
import datetime as dt

from mensapi.api.main import app
from mensapi.api.models import Dish, Allergens, Prices, Nutrients


def test_read_main(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Oliebe"}


def test_today_success(client, set_date, db_session):
    # Arrange
    set_date(dt.date(2026, 10, 5))
    monday = Dish(
            id=101,
            name="Veggie Wrap",
            day="Montag",
            date=dt.date(2026, 10, 5),
        )
    monday.prices = Prices(price_students=2.5, price_non_students=3.2)
    monday.nutrients = Nutrients(
        protein=8.22, fat=5.0, saturated_fat=0.8,
        kcal=210, kJ=880, carbohydrates=27.0, salt=0.7, sugar=3.5
    )
    monday.allergens = [Allergens(allergen_id=12, category="allergens", name="celery")]
    db_session.add(monday)
    db_session.commit()

    # Act
    response = client.get("/api/today")
    assert response.status_code == 200
    data = response.json()
    assert data[0]["name"] == "Veggie Wrap"
    assert data[0]["day"] == "Montag"

def test_id_success(client, db_session):
    # Arrange
    dish = Dish(
            id=34,
            name="Kichererbseneintopf",
            day="Dienstag",
            date=dt.date(2026, 10, 6),
        )
    dish.prices = Prices(price_students=3.3, price_non_students=4.1)
    dish.nutrients = Nutrients(
        protein=22.5, fat=12.0, saturated_fat=4.5,
        kcal=340, kJ=1420, carbohydrates=31.0, salt=1.2, sugar=2.0
    )
    dish.allergens = []
    db_session.add(dish)
    db_session.commit()

    # Act
    response = client.get("/api/dish/34")
    data = response.json()

    # Assert
    assert response.status_code == 200
    assert data[0]["id"] == 34 
    assert data[0]["name"] == "Kichererbseneintopf" 


def test_dish_not_found(client):
    response = client.get("/api/dish/27")

    assert response.status_code == 404
    assert response.json()["detail"] ==  "Dish not found under given id."


def test_today_saturday(client, today_dishes, set_date):
    set_date(dt.date(2026, 10, 3)) # Dependency inject Saturday
    response = client.get("/api/today")
    assert response.status_code == 200
    assert response.json() == {"detail": "There are no dishes on the weekend."}


def test_today_sunday(client, today_dishes, set_date):
    set_date(dt.date(2026, 10, 4)) # Dependency inject Sunday
    response = client.get("/api/today")
    assert response.status_code == 200
    assert response.json() == {"detail": "There are no dishes on the weekend."}

def test_week_current_thursday_success(client, set_date, db_current_dish_oli):
    set_date(dt.date(2026, 10, 7)) # Set Wednesday; Oli has the date (2026, 10, 8)

    response = client.get("/api/week/current/thursday")
    assert response.status_code == 200
    assert response.json()[0]["name"] == db_current_dish_oli.name


def test_week_current_empty(client, db_session):
    response = client.get("/api/week/current")
    assert response.status_code == 404 
    assert response.json()["detail"] ==  "Weekly dishes not found."


def test_week_next_thursday_success(client, set_date, db_current_dish_oli):
    set_date(dt.date(2026, 10, 3)) # Set Saturday; Oli has the date (2026, 10, 8)

    response = client.get("/api/week/next/thursday")
    assert response.status_code == 200
    assert response.json()[0]["name"] == db_current_dish_oli.name
    
def test_week_range_success(client, db_session):

    d1 = Dish(
        id=401,
        name="Early Dish",
        day="Montag",
        date=dt.date(2026, 9, 21),
    )
    d1.prices = Prices(price_students=1, price_non_students=2)
    d1.nutrients = Nutrients(
        protein=4, fat=1, saturated_fat=0.3,
        kcal=100, kJ=420, carbohydrates=12, salt=0.2, sugar=1,
    )
    d1.allergens = []

    d2 = Dish(
        id=402,
        name="Later Dish",
        day="Dienstag",
        date=dt.date(2026, 9, 24),
    )
    d2.prices = Prices(price_students=1.5, price_non_students=2.5)
    d2.nutrients = Nutrients(
        protein=5, fat=1.5, saturated_fat=0.4,
        kcal=120, kJ=500, carbohydrates=15, salt=0.3, sugar=2,
    )
    d2.allergens = []

    db_session.add_all([d1, d2])
    db_session.commit()

    response = client.get("/api/week?start=2026-09-21&end=2026-09-24")
    assert response.status_code == 200
    ids = {d["id"] for d in response.json()}
    assert ids == {401, 402}


def test_week_start_after_end_date(client):
    response = client.get("/api/week/?start=2026-09-24&end=2026-09-21")
    assert response.status_code == 400
    assert response.json() == {"detail":"The query parameter 'start' must be before or equal to 'end'."}


def test_week_empty(client, db_session):
    # db_session always returns an empty database
    response = client.get("/api/week/?start=2030-12-24&end=2030-12-31")
    assert response.status_code == 404
    assert response.json()["detail"] == "Weekly dishes not found."
