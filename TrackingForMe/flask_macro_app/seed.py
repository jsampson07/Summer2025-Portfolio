# Used for seeding the database and testing
from flask_macro_app import app, db
from flask_macro_app.models import User, Food, ServingUnit, GoalEnum, Meal
import sqlalchemy as sa
import click

food_staples_for_users = [
    {'name': "Chicken Breast", 'calories': 165, 'protein': 31, 'carbs': 0, 'fat': 4, 'serving_size': 100, 'serving_unit': ServingUnit.GRAMS},
    {'name': "Ground Turkey (93/7)", 'calories': 170, 'protein': 22, 'carbs': 0, 'fat': 9, 'serving_size': 100, 'serving_unit': ServingUnit.GRAMS},
    {'name': "Sirloin Steak", 'calories': 200, 'protein': 29, 'carbs': 0, 'fat': 9, 'serving_size': 100, 'serving_unit': ServingUnit.GRAMS},
    {'name': "Salmon", 'calories': 208, 'protein': 20, 'carbs': 0, 'fat': 13, 'serving_size': 100, 'serving_unit': ServingUnit.GRAMS},
    {'name': "Tilapia", 'calories': 96, 'protein': 20, 'carbs': 0, 'fat': 2, 'serving_size': 100, 'serving_unit': ServingUnit.GRAMS},
    {'name': "Cod", 'calories': 82, 'protein': 18, 'carbs': 0, 'fat': 1, 'serving_size': 100, 'serving_unit': ServingUnit.GRAMS},
    {'name': "Tuna", 'calories': 132, 'protein': 28, 'carbs': 0, 'fat': 1, 'serving_size': 100, 'serving_unit': ServingUnit.GRAMS},
    {'name': "Shrimp", 'calories': 99, 'protein': 24, 'carbs': 0, 'fat': 0, 'serving_size': 100, 'serving_unit': ServingUnit.GRAMS},
    {'name': "Egg (Large)", 'calories': 72, 'protein': 6, 'carbs': 0, 'fat': 5, 'serving_size': 1, 'serving_unit': ServingUnit.UNIT},
    {'name': "Egg Whites", 'calories': 52, 'protein': 11, 'carbs': 1, 'fat': 0, 'serving_size': 1, 'serving_unit': ServingUnit.UNIT},
    {'name': "Greek Yogurt (Plain)", 'calories': 170, 'protein': 15, 'carbs': 4, 'fat': 0, 'serving_size': 0.75, 'serving_unit': ServingUnit.CUP},
    {'name': "Cottage Cheese (Low Fat)", 'calories': 72, 'protein': 11, 'carbs': 3, 'fat': 1, 'serving_size': 100, 'serving_unit': ServingUnit.GRAMS},
    {'name': "Tofu", 'calories': 76, 'protein': 8, 'carbs': 2, 'fat': 5, 'serving_size': 100, 'serving_unit': ServingUnit.GRAMS},
    {'name': "Edamame", 'calories': 121, 'protein': 12, 'carbs': 10, 'fat': 5, 'serving_size': 1, 'serving_unit': ServingUnit.CUP},
    {'name': "Lentils", 'calories': 116, 'protein': 9, 'carbs': 20, 'fat': 0, 'serving_size': 1, 'serving_unit': ServingUnit.CUP},
    {'name': "Chickpeas", 'calories': 164, 'protein': 9, 'carbs': 27, 'fat': 3, 'serving_size': 1, 'serving_unit': ServingUnit.CUP},
    {'name': "Black Beans", 'calories': 132, 'protein': 9, 'carbs': 24, 'fat': 1, 'serving_size': 1, 'serving_unit': ServingUnit.CUP},
    {'name': "Whey Protein Powder", 'calories': 120, 'protein': 24, 'carbs': 3, 'fat': 1, 'serving_size': 1, 'serving_unit': ServingUnit.UNIT},
]

@click.command("seed")
def seed_database():
    """Seed the database with initial data."""
    db.drop_all()
    db.create_all()

    user1 = User(username="jsamp7", password="wasd123", email="jsamp7@example.com",
                 goal=GoalEnum.BULK)
    user2 = User(username="testdummy", password="securepass", email="dummy@example.com",
                 goal=GoalEnum.CASUAL)
    users = [user1, user2]
    db.session.add_all(users)
    db.session.commit()

    for food_data in food_staples_for_users:
        food = Food(
            name=food_data["name"],
            calories=food_data["calories"],
            protein=food_data["protein"],
            carbs=food_data["carbs"],
            fat=food_data["fat"],
            serving_size=food_data["serving_size"],
            serving_unit=food_data["serving_unit"]
        )
        db.session.add(food)

    db.session.commit()

    meal1 = Meal(name="Breakfast", user_id=user1.id)
    # How to add foods to the "foods" attribute of Meal ==> interact with the 'association table'
    query = sa.select(Food).where(Food.id.in_([1,2,3]))
    foods_for_meal = db.session.scalars(query).all()
    meal1.foods.extend(foods_for_meal)
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
    for food in foods:
        print(f"Food: {food.id}, Name: {food.name}, User_Owner: {food.user_id}")

    meal_query = sa.select(Meal)
    meals = db.session.scalars(meal_query).all()
    print(f"Meals: {meals}")

    first_meal_query = sa.select(Meal.id).order_by(Meal.id).limit(1).scalar_subquery()
    query = sa.select(Food).join(Meal.foods).where(Meal.id==first_meal_query)
    meal_items = db.session.scalars(query).all()
    for food in meal_items:
        print(f"ID: {food.id}, Food: {food.name}, Calories: {food.calories}")

    print("Done printing database")