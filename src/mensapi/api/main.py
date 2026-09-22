from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

import mensapi.api.models

from mensapi.api.schemas import DishResponse, PricesResponse, NutrientsResponse 
from mensapi.api.database import Base, engine, get_db

from typing import Annotated


app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/api/today", response_model=DishResponse) 
async def get_daily_menu(db: Annotated[Session, Depends(get_db)]) -> DishResponse:
    query_result = db.execute(
        select(models.Dish).where(models.User.date == datetime.now().date())
    )
    todays_dish = query_result.scalars().first()
    
    if todays_dish:
        return todays_dish

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Today's dish not found.")


@app.get("/api/{weekday}", response_model=DishResponse)
async def get_weekday_menu(weekday: str, db: Annotated[Session, Depends(get_db)]) -> DishResponse: 
    dish = db.get(DishResponse, weekday)
    if not dish:
        raise HTTPException(status_code=404, detail="Dish not found")
    return dish

@app.get("/api/week", response_model=list[DishResponse])
async def get_weekly_menu():
    pass
