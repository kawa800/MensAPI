from sqlalchemy.orm import Session 
from mensapi.api.database import engine
from mensapi.api.models import Dish, Nutrients, Allergens, Prices

def commit_data(dishes: list[Dish]):
    with Session(engine) as session:
        for dish in dishes:
            session.add(dish)
        session.commit()
