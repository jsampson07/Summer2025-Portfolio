# Used for seeding the database and testing
from flask_macro_app import app, db
from flask_macro_app.models import User, Food, ServingUnit, GoalEnum, Meal
import sqlalchemy as sa
import click

@click.command("seed")
def seed_database():
    """Seed the database with initial data."""
    user1 = User(username="jsamp7", password_hash="wasd123", email="jsamp7@example.com",
                 goal=GoalEnum.BULK)
    user2 = User(username="testdummy", password_hash="securepass", email="dummy@example.com",
                 goal=GoalEnum.CASUAL)
    users = [user1, user2]
    db.session.add_all(users)
    db.session.commit()

    food1 = Food(name="Chicken", calories=250, protein=25, serving_size=1,
                 serving_unit=ServingUnit.UNIT)
    food2 = Food(name="Whole Wheat Bread", calories=60, protein=8, carbs=13,
                 serving_size=1, serving_unit=ServingUnit.UNIT)
    food3 = Food(name="Cupcake", calories=150, carbs=25, fat=30,
                 serving_size=1, serving_unit=ServingUnit.UNIT,
                 user_id=user1.id)
    foods = [food1, food2, food3]
    db.session.add_all(foods)
    db.session.commit()

    meal1 = Meal(name="Breakfast", user_id=user1.id)
    # How to add foods to the "foods" attribute of Meal ==> interact with the 'association table'
    meal1.foods.extend(foods)
    db.session.add(meal1)
    db.session.commit()

    print("Done seeding database!")

@click.command("query")
def query_seed():
    print("Querying database")
    
    user_query = sa.select(User)
    users = db.session.scalars(user_query).all()
    print(f"Users: {users}")

    food_query = sa.select(Food)
    foods = db.session.scalars(food_query).all()
    print(f"Foods: {foods}")

    meal_query = sa.select(Meal)
    meals = db.session.scalars(meal_query).all()
    print(f"Meals: {meals}")

    print("Done printing database")