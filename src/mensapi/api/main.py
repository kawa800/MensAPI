from fastapi import Depends, FastAPI, HTTPException, status
from pydantic import BaseModel
import datetime as dt

from sqlalchemy import select
from sqlalchemy.orm import Session

import mensapi.api.models as models

from mensapi.api.schemas import DishResponse, PricesResponse, NutrientsResponse
from mensapi.api.database import Base, engine, get_db

from typing import Annotated


app = FastAPI()
# Dependency Injection
SessionDep = Annotated[Session, Depends(get_db)]


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/api/today", response_model=list[DishResponse]) 
async def get_daily_menu(db: SessionDep) -> list[DishResponse]:
    weekday = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"]
    current_day_index = dt.datetime.now().weekday()
    query_result = db.execute(select(models.Dish).where(models.Dish.day == weekday[current_day_index]))
    dish = query_result.scalars().all()
    if dish:
        return dish
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Today's dishes not found.")


@app.get("/api/{day}", response_model=DishResponse)
async def get_weekday_menu(day: str, db: Annotated[Session, Depends(get_db)]) -> DishResponse: 
    pass
    # dish = db.get(models.Dish, weekday)
    # if not dish:
    #     raise HTTPException(status_code=404, detail="Dish not found")
    # return dish


@app.get("/api/week", response_model=list[DishResponse])
async def get_weekly_menu(db: SessionDep) -> list[DishResponse]:
    result = db.execute(select(models.Dish))
    dishes = result.scalars().all()
    if dishes:
        return dishes
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Weekly dishes not found.")


@app.get("/api/dish/{id}", response_model=list[DishResponse])
async def get_dish_by_id(id: int, db: SessionDep) -> list[DishResponse]:
    result = db.execute(select(models.Dish).where(models.Dish.id == id))
    dishes = result.scalars().all()
    if dishes:
        return dishes
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dish not found.")


@app.get("/api/week/{start_date}-{end_date}", response_model=list[DishResponse])
async def get_weekly_menu(db: SessionDep, start_date: dt.date, end_date: dt.date) -> list[DishResponse]:
    result = db.execute(select(models.Dish))
    dishes = result.scalars().all()
    if dishes:
        return dishes
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Weekly dishes not found.")
