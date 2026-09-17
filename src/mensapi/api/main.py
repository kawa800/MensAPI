from fastapi import Depends, FastAPI
from pydantic import BaseModel

from mensapi.api.schemas import Dish, DailyMenu, WeeklyMenu

app = FastAPI()

async def test_injection(q: str | None = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/api/today", response_model=DailyMenu) 
async def get_daily_menu():
    return DailyMenu

@app.get("/api/{weekday}", response_model=DailyMenu)
async def get_weekday_menu(weekday: str):
    pass

@app.get("/api/week", response_model=WeeklyMenu)
async def get_weekly_menu():
    pass

