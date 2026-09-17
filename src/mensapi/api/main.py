from fastapi import Depends, FastAPI
from pydantic import BaseModel

from mensapi.api.schemas import Dish, DailyMenu, WeeklyMenu

app = FastAPI()

async def get_bolognese(q: str | None = None, skip: int = 0, limit: int = 100):
    expected_response = {
        "day": "Donnerstag",
        "date": "10.09.2026",
        "name": "Penne mit Sauce Bolognese",
        "price": {
            "Students": 2.40,
            "Non-Students": 4.50,
        },
        "nutrients": {
            "Protein": 26.4,
            "Fat": 25.53,
            "Saturated Fat": 6.42,
            "kcal": 734.85,
            "kJ": 3085.65,
            "Carbohydrates": 97.22,
            "Salt": 3.68,
            "Sugar": 11.77,
        },
        "allergens": [
            {
                "allergen_id": "8",
                "category": "allergens",
                "name": "gluten", 
            },
            {
                "allergen_id": "16",
                "category": "allergens",
                "name": "celery",
            },
            {
                "allergen_id": "20",
                "category": "allergens",
                "name": "wheat",
            },
            {
                "allergen_id": "14",
                "category": "additives",
                "name": "beef",
            },
        ],
    }
    return expected_response


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/api/today", response_model=DailyMenu) 
async def get_daily_menu() -> DailyMenu:
    return DailyMenu

@app.get("/api/{weekday}", response_model=DailyMenu)
async def get_weekday_menu(weekday: str):
    pass

@app.get("/api/week", response_model=WeeklyMenu)
async def get_weekly_menu():
    pass

