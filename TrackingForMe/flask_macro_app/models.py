from datetime import datetime
from typing import Optional
from flask_macro_app import db
import sqlalchemy as sa  # Used for fundamental building blocks for the database schema i.e. defining data types
import sqlalchemy.orm as so  # Used for functions and types that are part of the ORM's mapping proces (mapping objects)
import enum

class GoalEnum(enum.Enum):
    BULK = "bulk"
    CUT = "cut"
    MAINTAIN = "maintain"
    CASUAL = "casual"

class ServingUnit(enum.Enum):
    GRAMS = "g"
    OUNCE = "oz"
    ML = "ml"
    CUP = "cup"
    UNIT = "unit"

meal_items = db.Table("meal_items", db.Column("meal_id", db.Integer, db.ForeignKey("Meals.id"), primary_key=True),
                    db.Column("food_id", db.Integer, db.ForeignKey("Foods.id"), primary_key=True),
                    db.Column("quantity", db.Numeric(10,2)))

class User(db.Model):
    # so.Mapped[int]/so.Mapped[float] - defines the type of the column (required)
    # so.Mapped[Optional[str]] - defines type of the column should there be a value (not required)
    __tablename__ = "Users"  # __tablename__ for each class defines custom table name inside of database

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True,
                                                unique=True, nullable=False)
    password: so.Mapped[str] = so.mapped_column(sa.String(128), unique=False, nullable=False)  #ONLY NULLABLE FOR TESTING PURPOSES
    email: so.Mapped[str] = so.mapped_column(sa.String(128), index=True, unique=True, nullable=False)
    age: so.Mapped[int] = so.mapped_column(nullable=True)
    weight: so.Mapped[float] = so.mapped_column(nullable=True)
    goal: so.Mapped[GoalEnum] = so.mapped_column(sa.Enum(GoalEnum), nullable=True)  #NULLABLE ONLY FOR TESTING PURPOSES

    def __repr__(self):
        return f"<User {self.username}>"
    
class Food(db.Model):
    __tablename__ = "Foods"
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True, nullable=False)
    calories: so.Mapped[int] = so.mapped_column(nullable=False)
    protein: so.Mapped[int] = so.mapped_column(nullable=True)
    carbs: so.Mapped[int] = so.mapped_column(nullable=True)
    fat: so.Mapped[int] = so.mapped_column(nullable=True)
    serving_size: so.Mapped[float] = so.mapped_column(nullable=False)  # Must be provided, even if just 1 "unit"
    serving_unit: so.Mapped[ServingUnit] = so.mapped_column(sa.Enum(ServingUnit), nullable=False)

    user_id: so.Mapped[Optional[int]] = so.mapped_column(sa.ForeignKey("Users.id"), nullable=True)  # If food is in pre-existing catalog, no user id, else: userid of creator

    meals: so.Mapped[list["Meal"]] = so.relationship(secondary=meal_items, back_populates="foods")

    def __repr__(self):
        return f"<Food {self.name}>"
    
class Meal(db.Model):
    __tablename__ = "Meals"
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(128), unique=True, index=True, nullable=False)
    saved: so.Mapped[bool] = so.mapped_column(nullable=True, default=False)

    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey("Users.id"), nullable=False)  # Meal must be created by a user

    foods: so.Mapped[list["Food"]] = so.relationship(secondary=meal_items, back_populates="meals")

    def __repr__(self):
        return f"<Meal {self.name}>"
    
class DailyLog(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    log_date: so.Mapped[datetime] = so.mapped_column(sa.DateTime(), nullable=False, index=True)
    quantity_consumed: so.Mapped[float] = so.mapped_column(sa.Float, nullable=False, default=1)  # default store as 1 if "null"

    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey("Users.id"), nullable=False)  # Log entry must always correspond to a user
    food_id: so.Mapped[Optional[int]] = so.mapped_column(sa.ForeignKey("Foods.id"), nullable=True)
    meal_id: so.Mapped[Optional[int]] = so.mapped_column(sa.ForeignKey("Meals.id"), nullable=True)

    def __repr__(self):
        return f"<DailyLog {self.log_date}>"
