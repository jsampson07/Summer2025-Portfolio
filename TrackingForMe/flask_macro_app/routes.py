# Define routes and handlers for the endpoints
from flask_macro_app import app, db
from flask_macro_app.models import User, Food
from flask import jsonify, request
from typing import List, Dict, Any
import sqlalchemy as sa

@app.route('/api/foods')
def get_foods():
    query = sa.select(Food)
    sort_by = request.args.get("sort")
    
    if sort_by and hasattr(Food, sort_by):  # Do not assume that the attribute will exist
        query = query.order_by(getattr(Food, sort_by))
    # Either default sort or sort by some parameter
    foods = db.session.scalars(query).all()
    new_foods_list = []
    for food in foods:
        new_foods_list.append({
            "id": food.id,
            "name": food.name,
            "calories": food.calories,
            "protein": food.protein,
            "carbs": food.carbs,
            "fat": food.fat,
            "serving_size": food.serving_size,
            "serving_unit": str(food.serving_unit)
        })
        # Sort given the FOODS list for now
    return jsonify(new_foods_list) #wraps JSON output within Flask "Response" object -> sets Content-Type header auto to applicatin/json

@app.route('/api/register', methods=['POST'])
def create_user():
    print("Creating user...")


    
    print("Successfully created user!")

@app.route('/')
def test():
    return "Welcome to TrackingForMe, a macro-nutrient tracker to help you stay on track with your nutrition goals!"