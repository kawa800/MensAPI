from __future__ import annotations

from datetime import datetime, timezone, timedelta
from mensapi.api.database import Base

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

UTC_TWO = timezone(timedelta(hours=2))

class Dish(Base):
    __tablename__ = "dishes"

    id: Mapped[int] = mapped_column(primary_key=True)
    day: Mapped[str] = mapped_column(String(20), nullable=False)
    date: Mapped[datetime] = mapped_column(DateTime(timezone=True), default= lambda: datetime.now(UTC_TWO))
    name: Mapped[str] = mapped_column(String(255), nullable=False)

    nutrients: Mapped[Nutrients] = relationship(
        back_populates="dish",
        cascade="all, delete"
    )

    prices: Mapped[Prices] = relationship(
        back_populates="dish",
        cascade="all, delete"
    )

    allergens: Mapped[list[Allergens]] = relationship( # Allows for dish.allergens to return all allergens
        back_populates="dish",
        cascade="all, delete"
    ) 


class Prices(Base): 
    __tablename__ = "prices"
    id: Mapped[int] = mapped_column(primary_key=True)
    dish_id: Mapped[int] = mapped_column(
            ForeignKey("dishes.id"), 
            nullable=False,
            index=True,
            unique=True
    )

    price_students: Mapped[float] = mapped_column(Float)
    price_non_students: Mapped[float] = mapped_column(Float)

    dish: Mapped[Dish] = relationship(back_populates="prices")
    

class Nutrients(Base):
    __tablename__ = "nutrients"
    id: Mapped[int] = mapped_column(primary_key=True)
    dish_id: Mapped[int] = mapped_column(
            ForeignKey("dishes.id"), 
            nullable=False,
            index=True,
            unique=True # Because one dish has one set of nutrients
    )

    protein: Mapped[float] = mapped_column(Float, nullable=False)
    fat: Mapped[float] = mapped_column(Float, nullable=False)
    saturated_fat: Mapped[float] = mapped_column(Float, nullable=False)
    kcal: Mapped[float] = mapped_column(Float, nullable=False)
    kJ: Mapped[float] = mapped_column(Float, nullable=False)
    carbohydrates: Mapped[float] = mapped_column(Float, nullable=False)
    salt: Mapped[float] = mapped_column(Float, nullable=False)
    sugar: Mapped[float] = mapped_column(Float, nullable=False)

    dish: Mapped[Dish] = relationship(back_populates="nutrients")


class Allergens(Base):
    __tablename__ = "allergens"

    id: Mapped[int] = mapped_column(primary_key=True)
    dish_id: Mapped[int] = mapped_column(
            ForeignKey("dishes.id"), # foreign key, that links Allergens to Dish
            nullable=False,
            index=True,
    )

    # Allergen/Additives
    allergen_id: Mapped[int] = mapped_column() # Number infront of png, e.g. 18.png
    category: Mapped[str] = mapped_column(String(10), nullable=False) # allergens/additives
    name: Mapped[str] = mapped_column(String(255), nullable=False) # celery

    dish: Mapped[Dish] = relationship(back_populates="allergens")
