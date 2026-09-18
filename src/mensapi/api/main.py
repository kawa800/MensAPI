from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

import mensapi.api.models

from mensapi.api.schemas import DishResponse, PricesResponse, NutrientsResponse 

from typing import Annotated

app = FastAPI()

async def get_bolognese(q: str | None = None, skip: int = 0, limit: int = 100):
    return expected_response


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/api/today", response_model=DishResponse) 
async def get_daily_menu() -> DishResponse:
    result = db.execute(
        select(models.Dish).where(models.User.date == datetime.now().date())
    )
    todays_dish = result.scalars().first()
    
    if todays_dish:
        return todays_dish

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Today's dish not found.")


@app.get("/api/{weekday}", response_model=DishResponse)
async def get_weekday_menu(weekday: str):
    pass

@app.get("/api/week", response_model=list[DishResponse])
async def get_weekly_menu():
    pass
