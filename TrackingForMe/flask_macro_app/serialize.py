# Used to serialize return values in routes.py
from flask_macro_app import app,db
from flask_macro_app.models import User, Food, Meal, ServingUnit, GoalEnum, Meal_Food
from flask import jsonify

def serialize_user(user: User, created_at: str, og_email: str) -> dict:
    return {
        "id": user.id,
        "username": user.username,
        "email": og_email,
        "age": user.age,
        "weight": user.weight,
        "goal": user.goal.value if user.goal else None,
        "created_at": created_at
    }, 201

def serialize_food(food: Food) -> dict:
    return {
        "id": food.id,
        "name": food.name,
        "calories": food.calories,
        "protein": food.protein,
        "carbs": food.carbs,
        "fat": food.fat,
        "serving_size": food.serving_size,
        "serving_unit": food.serving_unit.value
    }

def serialize_make_food(food: Food, created_at: str):
    return {
        "id": food.id,
        "name": food.name,
        "calories": food.calories,
        "protein": food.protein,
        "carbs": food.carbs,
        "fat": food.fat,
        "serving_size": food.serving_size,
        "serving_unit": food.serving_unit.value,
        "created_at": created_at
    }

def serialize_meal_create(meal: Meal, created_at: str):
    total_calories = 0
    total_protein = 0
    total_carbs = 0
    total_fat = 0
    for meal_food in meal.food_items:
        total_calories+=(float(meal_food.food.calories)*float(meal_food.quantity))
        total_protein+=(float(meal_food.food.protein)*(meal_food.quantity))
        total_carbs+=(float(meal_food.food.carbs)*(meal_food.quantity))
        total_fat+=(float(meal_food.food.fat)*(meal_food.quantity))
    return {
        "id": meal.id,
        "name": meal.name,
        "saved": meal.saved,
        "total_calories": total_calories,
        "total_protein": total_protein if total_protein != 0 else "N/A",
        "total_carbs": total_carbs if total_carbs != 0 else "N/A",
        "total_fat": total_fat if total_fat != 0 else "N/A",
        "food_items": [
            {
                "id": meal_food.food.id,
                "name": meal_food.food.name,
                "quantity": meal_food.quantity
            } for meal_food in meal.food_items
        ],
        "created_at": created_at
    }

def serialize_meal_edit(meal: Meal, updated_at: str):
    total_calories = 0
    total_protein = 0
    total_carbs = 0
    total_fat = 0
    for meal_food in meal.food_items:
        total_calories+=(meal_food.food.calories*meal_food.quantity)
        total_protein+=(meal_food.food.protein*meal_food.quantity)
        total_carbs+=(meal_food.food.carbs*meal_food.quantity)
        total_fat+=(meal_food.food.fat*meal_food.quantity)
    return {
        "id": meal.id,
        "name": meal.name,
        "saved": meal.saved,
        "total_calories": total_calories,
        "total_protein": total_protein if total_protein != 0 else "N/A",
        "total_carbs": total_carbs if total_carbs != 0 else "N/A",
        "total_fat": total_fat if total_fat != 0 else "N/A",
        "food_items": [
            {
                "id": meal_food.food.id,
                "name": meal_food.food.name,
                "quantity": meal_food.quantity
            } for meal_food in meal.food_items
        ],
        "updated_at": updated_at
    }

def serialize_meal(meal: Meal):
    total_calories = 0
    total_protein = 0
    total_carbs = 0
    total_fat = 0
    for meal_food in meal.food_items:
        food = meal_food.food
        qty = meal_food.quantity
        calories = food.calories or 0
        protein = food.protein or 0
        carbs = food.carbs or 0
        fat = food.fat or 0
        total_calories+=(calories*qty)
        total_protein+=(protein*qty)
        total_carbs+=(carbs*qty)
        total_fat+=(fat*qty)
    return {
        "id": meal.id,
        "name": meal.name,
        "total_calories": total_calories,
        "total_protein": total_protein,
        "total_carbs": total_carbs,
        "total_fat": total_fat
    }

def serialize_meal_patch(meal_food: Meal_Food, updated_at: str):
    return {
        "food_id": meal_food.food_id,
        "food_name": meal_food.food.name,
        "quantity": meal_food.quantity
    }

def serialize_meal_food(meal_food: Meal_Food):
    food_data = serialize_food(meal_food.food)
    food_data["quantity"] = meal_food.quantity
    return food_data