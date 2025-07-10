# Used to serialize return values in routes.py
from flask_macro_app import app,db
from flask_macro_app.models import User, Food, Meal, ServingUnit, GoalEnum
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