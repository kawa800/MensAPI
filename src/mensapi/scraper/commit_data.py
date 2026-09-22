from sqlalchemy.orm import Session 
from mensapi.api.database import engine
from mensapi.api.models import Dish, Nutrients, Allergens, Prices

def commit_data(scraped_meals: list[dict]):
    with Session(engine) as session:
        for meal in scraped_meals:
            dish = Dish(
                day = meal["day"],
                date = meal["date"],
                name = meal["name"],
                nutrients = Nutrients(
                    protein = meal["nutrients"]["Protein"],
                    fat = meal["nutrients"]["Fat"],
                    saturated_fat = meal["nutrients"]["Saturated Fat"],
                    kcal = meal["nutrients"]["kcal"],
                    kJ = meal["nutrients"]["kJ"],
                    carbohydrates = meal["nutrients"]["Carbohydrates"],
                    salt = meal["nutrients"]["Salt"],
                    sugar = meal["nutrients"]["Sugar"]
                ),
                prices = Prices(
                    price_students = meal["price"]["Students"],
                    price_non_students = meal["price"]["Non-Students"]
                ),
                allergens = [Allergens(allergen_id = a["allergen_id"], category = a["category"], name = a["name"]) for a in meal["allergens"]]
            )
            session.add(dish)
        session.commit()
