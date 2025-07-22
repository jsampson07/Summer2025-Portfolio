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
        total_calories+=meal_food.food.calories
        total_protein+=meal_food.food.protein
        total_carbs+=meal_food.food.carbs
        total_fat+=meal_food.food.fat
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
        total_calories+=meal_food.food.calories
        total_protein+=meal_food.food.protein
        total_carbs+=meal_food.food.carbs
        total_fat+=meal_food.food.fat
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
    for meal_food in meal.food_items:
        total_calories+=meal_food.food.calories
    return {
        "id": meal.id,
        "name": meal.name,
        "total_calories": total_calories
    }