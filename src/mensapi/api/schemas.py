# Define what data the API can expose. Pydantic then validates that the data matches the definitions.
<<<<<<< HEAD
from __future__ import annotations
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

expected_response = {
    "day": "Donnerstag",
    "date": "10.09.2026",
    "name": "Orientalischer Linseneintopf mit Kokosmilch",
    "prices": {
        "Students": 1.80,
        "Non-Students": 3.40,
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


class DishResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True, # allow returning ORM-models
        json_schema_extra={ "example": expected_response } # display expected JSON output in OpenAPI docs
    )

    id: int = Field(examples=[1])
    day: str = Field(examples=["Donnerstag"])
    date: datetime = Field(examples=["18.09.2026"])
    name: str = Field(examples=["Orientalischer Linseneintopf"])

    nutrients: NutrientsResponse
    prices: PricesResponse
    allergens: list[AllergensResponse]

class PricesResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True) # allow reading from objects using dot-notation

    price_students: float = Field(examples=[1.80])
    price_non_students: float = Field(examples=[3.40])

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

class NutrientsResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True) # allow reading from objects using dot-notation

    protein: float = Field(examples=[25.8])
    fat: float = Field(examples=[13.4])
    saturated_fat: float = Field(examples=[10.4])
    kcal: float = Field(examples=[518])
    kJ: float = Field(examples=[2167])
    carbohydrates: float = Field(examples=[68.0])
    salt: float = Field(examples=[8.4])
    sugar: float = Field(examples=[8.6])

class AllergensResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    allergen_id: int = Field(examples=[16])
    category: str = Field(examples=["allergens"])
    name: str = Field(examples=["celery"])
