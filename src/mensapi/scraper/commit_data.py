from sqlalchemy import select
from sqlalchemy.orm import Session 
from mensapi.api.database import engine
from mensapi.api.models import Dish, Nutrients, Allergens, Prices

def commit_data(dishes: list[Dish]):
    with Session(engine) as session:
        for dish in dishes:

            similar_dish = select(Dish).where(
                    Dish.date == dish.date,
                    Dish.name == dish.name,
            )

            existing = session.scalar(similar_dish)

            print(
                "CHECKING DUPLICATES:",
                dish.date,
                repr(dish.name),
                "FOUND:",
                existing
            )

            if existing is None:
                session.add(dish)
                session.flush()
                continue


            # Update Dish if it has changed on the second scraping run
            if dish.prices:
                existing.prices.price_students = dish.prices.price_students
                existing.prices.price_non_students = dish.prices.price_non_students

            if dish.nutrients:
                existing.nutrients.protein = dish.nutrients.protein
                existing.nutrients.fat = dish.nutrients.fat
                existing.nutrients.saturated_fat = dish.nutrients.saturated_fat
                existing.nutrients.kcal = dish.nutrients.kcal
                existing.nutrients.kJ = dish.nutrients.kJ
                existing.nutrients.carbohydrates = dish.nutrients.carbohydrates
                existing.nutrients.salt = dish.nutrients.salt
                existing.nutrients.sugar = dish.nutrients.sugar

            existing.allergens.clear()
            for allergen in dish.allergens:
                existing.allergens.append(
                    Allergens(
                        allergen_id=allergen.allergen_id,
                        category=allergen.category,
                        name=allergen.name,
                    )
                )


        session.commit()
