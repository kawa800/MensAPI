# Define what data the API can expose. Pydantic then validates that the data matches the definitions.
from __future__ import annotations
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class DishResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True) # allow reading from objects using dot-notation

    id: int
    day: str
    date: datetime
    name: str

    nutrients: NutrientsResponse
    prices: PricesResponse
    allergens: list[AllergensResponse]

class PricesResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True) # allow reading from objects using dot-notation

    price_students: float
    price_non_students: float

class NutrientsResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True) # allow reading from objects using dot-notation

    protein: float
    fat: float
    saturated_fat: float
    kcal: float
    kJ: float
    carbohydrates: float
    salt: float
    sugar: float

class AllergensResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    allergen_id: int
    category: str
    name: str
