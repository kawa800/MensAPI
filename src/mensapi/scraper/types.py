from typing import TypedDict

class Allergen(TypedDict):
    allergen_id: str
    category: str
    name: str

class Nutrition(TypedDict):
    Protein: float
    Fat: float
    SaturatedFat: float
    kcal: float
    kJ: float
    Carbohydrates: float
    Salt: float
    Sugar: float

class Price(TypedDict):
    Students: float
    NonStudents: float

class Dish(TypedDict):
    meal: str
    price: Price
    nutrition: Nutrition
    allergens: list[Allergen]

class DailyMenu(TypedDict):
    day: str
    date: str
    dishes: list[Dish]
