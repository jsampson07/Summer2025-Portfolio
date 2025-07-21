from datetime import datetime
from typing import Optional, Literal
from flask_macro_app import db
import sqlalchemy as sa  # Used for fundamental building blocks for the database schema i.e. defining data types
import sqlalchemy.orm as so  # Used for functions and types that are part of the ORM's mapping proces (mapping objects)
import enum
from werkzeug.security import generate_password_hash, check_password_hash

from pydantic import BaseModel, Field, EmailStr

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

class RegisterInput(BaseModel):
    username: str = Field(..., min_length=6, max_length=64)
    password: str = Field(..., min_length=4)  # FOR TESTING ONLY !!! IN production = 14
    email: EmailStr = Field(..., max_length = 128)
    age: Optional[int] = Field(default=None, ge=0)
    weight: Optional[float] = Field(default=None, ge=0)
    goal: Optional[GoalEnum] = None

class LoginInput(BaseModel):
    username: str = Field(..., min_length=6, max_length=64)
    password: str = Field(..., min_length=4)

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

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f"<User {self.username}>"
    
class FoodCreateEdit(BaseModel):
    name: str = Field(..., min_length=2, max_length=64)
    calories: int = Field(..., ge=0)
    protein: Optional[int] = Field(default=0, ge=0)
    carbs: Optional[int] = Field(default=0, ge=0)
    fat: Optional[int] = Field(default=0, ge=0)
    serving_size: float = Field(..., gt=0)
    serving_unit: ServingUnit = Field(...)
    
class Food(db.Model):
    __tablename__ = "Foods"
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, nullable=False)
    calories: so.Mapped[int] = so.mapped_column(nullable=False)
    protein: so.Mapped[int] = so.mapped_column(nullable=True)
    carbs: so.Mapped[int] = so.mapped_column(nullable=True)
    fat: so.Mapped[int] = so.mapped_column(nullable=True)
    serving_size: so.Mapped[float] = so.mapped_column(nullable=False)  # Must be provided, even if just 1 "unit"
    serving_unit: so.Mapped[ServingUnit] = so.mapped_column(sa.Enum(ServingUnit), nullable=False)

    user_id: so.Mapped[Optional[int]] = so.mapped_column(sa.ForeignKey("Users.id"), nullable=True)  # If food is in pre-existing catalog, no user id, else: userid of creator

    meal_items: so.Mapped[list["Meal_Food"]] = so.relationship(back_populates="food", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Food {self.name}>"
    
class Meal(db.Model):
    __tablename__ = "Meals"
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(128), index=True, nullable=False)
    saved: so.Mapped[bool] = so.mapped_column(nullable=True, default=False)

    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey("Users.id"), nullable=False)  # Meal must be created by a user

    food_items: so.Mapped[list["Meal_Food"]] = so.relationship(back_populates="meal", cascade="all, delete-orphan")  # A meal has many foods

    def __repr__(self):
        return f"<Meal {self.name}>"

class Meal_Food(db.Model):
    __tablename__ = "Meal_Food"
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    food_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey("Foods.id"), nullable=False)
    meal_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey("Meals.id"), nullable=False)
    quantity: so.Mapped[float] = so.mapped_column(nullable=False)

    food: so.Mapped["Food"] = so.relationship(back_populates="meal_items")
    meal: so.Mapped["Meal"] = so.relationship(back_populates="food_items")

    def __repr__(self):
        return f"<Meal_Food {self.food.name} {self.meal.name}>"
    
class MealFoodInput(BaseModel):
    food_id: int = Field(...)
    quantity: float = Field(..., gt=0)
    
class MealCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=64)
    saved: bool = Field(default=False)
    food_items: list[MealFoodInput] = Field(..., min_length=1)
    
class DailyLog(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    log_date: so.Mapped[datetime] = so.mapped_column(sa.DateTime(), nullable=False, index=True)
    quantity_consumed: so.Mapped[float] = so.mapped_column(sa.Float, nullable=False, default=1)  # default store as 1 if "null"

    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey("Users.id"), nullable=False)  # Log entry must always correspond to a user
    food_id: so.Mapped[Optional[int]] = so.mapped_column(sa.ForeignKey("Foods.id"), nullable=True)
    meal_id: so.Mapped[Optional[int]] = so.mapped_column(sa.ForeignKey("Meals.id"), nullable=True)

    def __repr__(self):
        return f"<DailyLog {self.log_date}>"
