from fastapi import Depends, FastAPI, HTTPException, Query, status
from pydantic import BaseModel
import datetime as dt

from sqlalchemy import select
from sqlalchemy.orm import Session

import mensapi.api.models as models

from mensapi.api.docs.examples import WEEKLY_MENU_EXAMPLE
from mensapi.api.schemas import DishResponse, PricesResponse, NutrientsResponse
from mensapi.api.database import Base, engine, get_db

from typing import Annotated


app = FastAPI()
# Dependency Injection
SessionDep = Annotated[Session, Depends(get_db)]
# Week offsets in German for /api/week/{day} endpoint
OFFSET = {
            "montag": 0, "dienstag": 1, "mittwoch": 2, "donnerstag": 3, "freitag": 4, "samstag": 5, "sonntag": 6,
            "monday": 0, "tuesday": 1, "wednesday": 2, "thursday": 3, "friday": 4, "saturday": 5, "sunday": 6
         }


@app.get("/")
async def root():

    return {"message": "Oliebe"}


@app.get("/api/today", response_model=list[DishResponse]) 
async def get_daily_menu(db: SessionDep) -> list[DishResponse]:
    """ Get today's Menu. """
    weekday = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"]
    current_day_index = dt.datetime.now().weekday()
    query_result = db.execute(select(models.Dish).where(models.Dish.day == weekday[current_day_index]))
    dish = query_result.scalars().all()
    if dish:
        return dish
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Today's dishes not found.")


@app.get("/api/dish/{id}", response_model=list[DishResponse])
async def get_dish_by_id(id: int, db: SessionDep) -> list[DishResponse]:
    """ Get a Dish by a specific id. """
    result = db.execute(select(models.Dish).where(models.Dish.id == id))
    dishes = result.scalars().all()
    if dishes:
        return dishes
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dish not found.")


@app.get("/api/week/current", response_model=list[DishResponse], responses= {200: {"content": {"application/json": {"example": WEEKLY_MENU_EXAMPLE}}}})
async def get_weekly_menu(db: SessionDep) -> list[DishResponse]:
    """ Get the Weekly Menu of the current week. """
    result = db.execute(select(models.Dish))
    dishes = result.scalars().all()
    if dishes:
        return dishes
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Weekly dishes not found.")


@app.get("/api/week/{day}", response_model=list[DishResponse])
async  def get_weekday_menu(day: str, db: Annotated[Session, Depends(get_db)]) -> list[DishResponse]: 
    """ Get the Daily Menu of day in the current week. """
    day_lower = day.lower()
    if day_lower not in OFFSET:
        raise HTTPException(
            status_code=status.HTTP_404_BAD_REQUEST,
            detail=f"Invalid day {day}. Use in the format: /api/week/montag or /api/week/monday."
        )

    today = dt.datetime.today()
    start_of_week = today - dt.timedelta(days=today.weekday())

    offset = OFFSET[day_lower]
    target_day = start_of_week + dt.timedelta(days=offset)
    print(target_day)

    result = db.execute(select(models.Dish).where(models.Dish.date == target_day.date()))
    dishes = result.scalars().all()
    if dishes:
        return dishes
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dish not found.")



@app.get("/api/week", response_model=list[DishResponse])
async def get_weekly_menu(db: SessionDep, start: dt.date = Query(examples=["2026-09-21"]), end: dt.date = Query(examples=["2026-09-24"])) -> list[DishResponse]:
    """ Get the Daily Menu of days in the range of start_date to inclusive end_date. """
    if start > end:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The query parameter 'start' must be before or equal to 'end'.",
        )
    result = db.execute(select(models.Dish).where(models.Dish.date.between(start, end)))
    dishes = result.scalars().all()
    if dishes:
        return dishes
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Weekly dishes not found.")
