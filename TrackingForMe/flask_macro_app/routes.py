# Define routes and handlers for the endpoints
from flask_macro_app import app, db
from flask_macro_app.models import User, Food
from flask import jsonify, request, Flask
from typing import List, Dict, Any
import sqlalchemy as sa
from datetime import datetime
from sqlalchemy.exc import IntegrityError

from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager


@app.route('/api/login', methods=['POST'])
def login():
    # After a successful login, this route should return a JWT (JSON Web Token). Once that's working,
    # you should use JWTs to protect your existing /api/foods route and any new routes you build.
    """
    Format: {
        "username": ..., (OPTIONAL)
        "password": ..., (REQUIRED)
    }    """
    user_data = request.get_json()
    if (not user_data) or (not all(key in user_data for key in ['username', 'password'])):
        return jsonify({"error_message": "Missing required fields: username, password"}), 400
    username = user_data.get("username", None)
    password = user_data.get("password")
    user_lookup = db.session.scalar(sa.Select(User).where(User.username == username))
    if (not user_lookup) or (not user_lookup.check_password(password)):
        return jsonify({"error_message": "Invalid username or password"}), 401
    access_tok = create_access_token(identity=user_lookup.id)
    return jsonify(access_token=access_tok)

@app.route('/api/register', methods=['POST'])
def create_user():
    user_data = request.get_json()
    if (not user_data) or (not all(key in user_data for key in ['username', 'password', 'email'])):
        return jsonify({"error_message": "Missing required fields: username, password, email"}), 400
    print("Creating user...")

    #REMEMBER --> EVERYTHING IS SENT VIA JSON FORMAT inside the crafted requests and response bodies
    username = user_data["username"]
    password = user_data["password"]  # NOTE: have not implemented hashing yet!!!!
    email = user_data["email"]
    age = user_data.get("age")
    weight = user_data.get("weight")
    goal = user_data.get("goal")

    user_query = sa.Select(User).where(User.username == username)
    email_query = sa.Select(User).where(User.email == email)
    if db.session.scalar(user_query):
        return jsonify({"error_message": "Username already exists"}), 409
    if db.session.scalar(email_query):
        return jsonify({"error_message": "Email is already in use"}), 409

    new_user = User(
        username=username,
        email=email,
        age=age,
        weight=weight,
        goal=goal
    )
    new_user.set_password(password)

    try:
        db.session.add(new_user)
        db.session.commit()
        date_time = datetime.datetime.now()
        formatted = date_time.isoformat()
        print("Successfully created user!")
        return jsonify({
            "id": new_user.id,
            "username": new_user.username,
            "email": new_user.email,
            "age": new_user.age,
            "weight": new_user.weight,
            "goal": new_user.goal,
            "created_at": formatted
        })
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({"error_message": "Username or email already exists"}), 400
    except:
        db.session.rollback()
        return jsonify({"error_message": "Could not add you as a user. Please try again."}), 500

#Get all foods for the logged-in user
@app.route('/api/foods', methods=['GET', 'POST'])
@jwt_required()
def get_all_foods():
    current_user_id = get_jwt_identity()

    if request.method == 'GET':

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

@app.route('/api/foods/<int:food_id>', methods=['GET', 'PATCH', 'DELETE'])
@jwt_required()
def get_one_food(food_id):
    current_user_id = get_jwt_identity()

@app.route('/api/profile', methods=["PATCH"])
def update_user():
    user_data = request.get_json()
    print(f"receieved: {user_data}")
    username = user_data["username"]
    password = user_data["password"]  # NOTE: have not implemented hashing yet!!!!
    email = user_data["email"]
    age = user_data.get("age")
    weight = user_data.get("weight")
    goal = user_data.get("goal")
    return

@app.route('/')
def test():
    return "Welcome to TrackingForMe, a macro-nutrient tracker to help you stay on track with your nutrition goals!"