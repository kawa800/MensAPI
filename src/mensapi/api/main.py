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
# Dependency Injections
SessionDep = Annotated[Session, Depends(get_db)] # Database

def current_date() -> dt.date: # Date
    """ Return the current date. Dependency Injection for get_today """
    return dt.date.today()

# Week offsets in German for /api/week/{day} endpoint
OFFSET = {
            "montag": 0, "dienstag": 1, "mittwoch": 2, "donnerstag": 3, "freitag": 4, "samstag": 5, "sonntag": 6,
            "monday": 0, "tuesday": 1, "wednesday": 2, "thursday": 3, "friday": 4, "saturday": 5, "sunday": 6
         }



@app.get("/")
async def root():
    return {"message": "Oliebe"}
    

@app.get("/api/today", response_model=list[DishResponse]) 
async def get_today(db: SessionDep, today: dt.date = Depends(current_date)) -> list[DishResponse]:
    """ Get today's Menu. """
    if today.weekday() >= 5:
        raise HTTPException(status_code=status.HTTP_200_OK, detail="There are no dishes on the weekend.")

    weekday = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"]
    current_day_index = today.weekday()
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
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dish not found under given id.")


@app.get("/api/week/current", response_model=list[DishResponse], responses= {200: {"content": {"application/json": {"example": WEEKLY_MENU_EXAMPLE}}}})
async def get_weekly_menu(db: SessionDep) -> list[DishResponse]:
    """ Get the Weekly Menu of the current week. """
    result = db.execute(select(models.Dish))
    dishes = result.scalars().all()
    if dishes:
        return dishes
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Weekly dishes not found.")


def _resolve_day(day: str, offset_days: int, today: dt.date = Depends(current_date)) -> dt.date:
    day_lower = day.lower()
    if day_lower not in OFFSET:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid day {day}. Use in the format: /api/week/current/montag or /api/week/current/monday."
        )

    start_of_week = today - dt.timedelta(days=today.weekday())

    target_day = start_of_week + dt.timedelta(days=OFFSET[day_lower] + offset_days)
    return target_day


@app.get("/api/week/current/{day}", response_model=list[DishResponse])
async  def get_current_week_menu(day: str, db: Annotated[Session, Depends(get_db)], today: dt.date = Depends(current_date)) -> list[DishResponse]: 
    """ Get the Daily Menu of day in the current week. """
    target_day = _resolve_day(day, 0, today)
    result = db.execute(select(models.Dish).where(models.Dish.date == target_day))
    dishes = result.scalars().all()
    if dishes:
        return dishes
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dish not found.")


@app.get("/api/week/next/{day}", response_model=list[DishResponse])
async  def get_next_week_menu(day: str, db: Annotated[Session, Depends(get_db)], today: dt.date = Depends(current_date)) -> list[DishResponse]: 
    """ Get the Daily Menu of day in the next week. """
    target_day = _resolve_day(day, 7, today)
    result = db.execute(select(models.Dish).where(models.Dish.date == target_day))
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
