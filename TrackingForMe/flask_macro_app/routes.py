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
    elif sort_by and (not hasattr(Food, sort_by)):
        error_payload = {
            "status": "error",
            "message": f"'{sort_by}' is not a valid field to sort by"
        }
        return jsonify(error_payload), 400
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

    #REMEMBER --> EVERYTHING IS SENT VIA JSON FORMAT inside the crafted requests and response bodies
    user_data = request.get_json()
    print(f"receieved: {user_data}")
    username = user_data["username"]
    password_pt = user_data["password"]  # NOTE: have not implemented hashing yet!!!!
    email = user_data["email"]
    age = user_data.get("age")
    weight = user_data.get("weight")
    goal = user_data.get("goal")

    new_user = User(
        username=username,
        password_hash=password_pt,
        email=email,
        age=age,
        weight=weight,
        goal=goal
    )

    try:
        db.session.add(new_user)
        db.session.commit()
        #return jsonify()
    except:
        return jsonify({"error_message": "Could not add you as a user. Please try again."}), 400
    
    print("Successfully created user!")

@app.route('/')
def test():
    return "Welcome to TrackingForMe, a macro-nutrient tracker to help you stay on track with your nutrition goals!"