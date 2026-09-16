from pydantic import BaseModel


class Dish(pydantic.BaseModel):
    name: str
    price: dict[str,float]
    nutrients: dict[str,float]
    allergens: list[dict[str,str]]

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "day": "Donnerstag",
                    "description": "Orientalischer Linseneintopf mit Kokosmilch",
                    "price": {
                        "Students": 1.80,
                        "Non-Students": 3.40
                    },
                    "nutrients": {
                        "Protein": 25.81,
                        "Fat": 13.43,
                        "Saturated Fat": 9.2,
                        "kcal": 517.52,
                        "kJ": 2173.09,
                        "Carbohydrates": 67.99,
                        "Salt": 8.43, 
                        "Sugar": 12.19
                    },
                    "allergens": [
                        {"allergen_id": 16, 
                         "category": "allergens",
                         "name": "celery"
                         }
                    ]
                }
            ]
        }
    }


class DailyMenu(pydantic.BaseModel):
    day: str
    date: str
    name: list[Dish] 


class WeeklyMenu(pydantic.BaseModel):
    days: list[DailyMenu]

