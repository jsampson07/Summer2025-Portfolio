# Define routes and handlers for the endpoints
from flask_macro_app import app, db
from flask_macro_app.models import User, Food, ServingUnit, GoalEnum, RegisterInput, LoginInput, FoodCreateEdit, MealCreate, Meal, Meal_Food, MealFoodInput
from flask import jsonify, request, Flask
from typing import List, Dict, Any
import sqlalchemy as sa
from sqlalchemy import or_, and_
from datetime import datetime, timezone
from sqlalchemy.exc import IntegrityError

from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required

import logging
from logging.handlers import RotatingFileHandler
import os

from pydantic import ValidationError

from flask_macro_app.serialize import serialize_user, serialize_food, serialize_make_food, serialize_meal_create, serialize_meal, serialize_meal_edit

if not os.path.exists('logs'):
    os.mkdir('logs')

file_handler = RotatingFileHandler('logs/app.log', maxBytes=10240, backupCount=10)
file_handler.setFormatter(logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
))
file_handler.setLevel(logging.INFO)

app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)
app.logger.info("Running application...")


@app.route('/api/login', methods=['POST'])
def login():
    # After a successful login, this route should return a JWT (JSON Web Token). Once that's working,
    # you should use JWTs to protect your existing /api/foods route and any new routes you build.
    try:
        user_data = LoginInput(**request.get_json())
    except ValidationError as e:
        return jsonify({"error_message": e.errors()}), 400
    username = user_data.username
    password = user_data.password
    user_lookup = db.session.scalar(sa.Select(User).where(User.username == username))
    if (not user_lookup) or (not user_lookup.check_password(password)):
        return jsonify({"error_message": "Invalid username or password"}), 401
    access_tok = create_access_token(identity=str(user_lookup.id))
    return jsonify(access_token=access_tok)

@app.route('/api/register', methods=['POST'])
def register():
    try:
        user_data = RegisterInput(**request.get_json())
    except ValidationError as e:
        return jsonify({"error_message": e.errors()}), 400
    print("Creating user...")

    #REMEMBER --> EVERYTHING IS SENT VIA JSON FORMAT inside the crafted requests and response bodies
    username = user_data.username
    password = user_data.password  # NOTE: have not implemented hashing yet!!!!
    email_front_end = user_data.email
    email = email_front_end.lower()
    age = user_data.age
    weight = user_data.weight
    goal = user_data.goal

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
        date_time = datetime.now(timezone.utc).isoformat()  # Avoids timezone issues
        return jsonify(serialize_user(new_user, date_time, email_front_end)), 201
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({"error_message": "Username or email already exists"}), 400
    except Exception as e:
        db.session.rollback()
        print(f"An unexpected error occurred: {e}")
        return jsonify({"error_message": "Could not add you as a user. Please try again."}), 500


#Get all foods for the logged-in user
@app.route('/api/foods', methods=['GET', 'POST'])
@jwt_required()
def get_all_foods():
    current_user_id = int(get_jwt_identity())  # Returns string MUST CAST

    if request.method == 'GET':  # Retrieve list of all foods that user can access

        query = sa.select(Food).where(or_(Food.user_id == current_user_id, Food.user_id.is_(None)))
        sort_by = request.args.get("sort")
        
        if sort_by in ["calories", "protein", "carbs", "fat"]:  # Do not assume that the attribute will exist
            query = query.order_by(getattr(Food, sort_by))
        elif sort_by and (not hasattr(Food, sort_by)):
            return jsonify({"error_message": f"'{sort_by}' is not a valid field to sort by"}), 400
        # Either default sort or sort by some parameter
        foods = db.session.scalars(query).all()
        return jsonify([serialize_food(food) for food in foods]), 200

    if request.method == 'POST':  # Create a new food item for user
        try:
            user_data = FoodCreateEdit(**request.get_json())
        except ValidationError as e:
            return jsonify({"error_message": e.errors()}), 400
        
        name = user_data.name
        calories = user_data.calories
        protein = user_data.protein
        carbs = user_data.carbs
        fat = user_data.fat
        serving_size = user_data.serving_size
        serving_unit = user_data.serving_unit

        food_query = sa.Select(Food).where(and_(Food.name == name, Food.user_id == current_user_id))

        if db.session.scalar(food_query):
            return jsonify({"error_message": f"'{name}' already exists"}), 409
            # Perhaps now give option to edit the food item instead

        new_food = Food(
            name=name,
            calories=calories,
            protein=protein,
            carbs=carbs,
            fat=fat,
            serving_size=serving_size,
            serving_unit=serving_unit,
            user_id=current_user_id
        )

        print("name:", new_food.name)
        print("calories:", new_food.calories)
        print("protein:", new_food.protein)
        print("carbs:", new_food.carbs)
        print("fat:", new_food.fat)
        print("serving_size:", new_food.serving_size)
        print("serving_unit_enum:", new_food.serving_unit)
        print("user_id:", new_food.user_id)

        try:
            print("WE HAVE ENTERED HERE!!!!")
            db.session.add(new_food)
            db.session.commit()
            print("WE HAVE FINISHED ADDING TO DB")
            date_time = datetime.now(timezone.utc).isoformat()
            print("Successfully created food")
            return jsonify(serialize_make_food(new_food, date_time)), 201
        except Exception as e:
            db.session.rollback()
            import traceback
            print("Exception during DB commit: ", e)
            traceback.print_exc()
            return jsonify({"error_message": "Unexpected error occurred"}), 500


@app.route('/api/foods/<int:food_id>', methods=['GET', 'PATCH', 'DELETE'])
@jwt_required()
def get_one_food(food_id):
    current_user_id = int(get_jwt_identity())
    food_item = db.session.get(Food, food_id)  # Use across all methods
    print(food_item)
    if not food_item:
        return jsonify({"error_message": "Food not found"}), 404

    if request.method == 'GET':  # Get specified food item
        permissions = (food_item.user_id == current_user_id
                       or food_item.user_id is None)
        if not permissions:
            return jsonify({"error_message": "Permission denied"}), 403
        
        return jsonify(serialize_food(food_item)), 200

    if request.method == 'DELETE':  # Delete food item from user's database
        # Only want to be able to delete foods that have Food.userid == current_user_id
        #query = sa.Select(Food).where(Food.id == food_id and Food.user_id == current_user_id)
        #food_to_delete = db.session.scalar(query)
        print(food_item.user_id)
        print(current_user_id)
        if food_item.user_id == current_user_id:  # We have permission
            try:
                db.session.delete(food_item)
                db.session.commit()
                return '', 204
            except Exception:
                db.session.rollback()
                return jsonify({"error_message": "Unexpected error occurred"}), 500
        else:
            return jsonify({"error_message": "Permission denied"}), 403
        
    if request.method == 'PATCH':  # Edit fields of a food item that corresponds to user
        # Update a food entry with newly provided user information (ONLY for Food.user_id == current_user_id)
        if food_item.user_id == current_user_id:
            try:
                user_data = FoodCreateEdit(**request.get_json())
                food_item.name = user_data.name
                food_item.calories = user_data.calories
                food_item.protein = user_data.protein
                food_item.carbs = user_data.carbs
                food_item.fat = user_data.fat
                food_item.serving_size = user_data.serving_size
                food_item.serving_unit = user_data.serving_unit
                
                #food_item.serving_unit = user_data.get("serving_unit", food_item.serving_unit)

                db.session.commit()

                return jsonify(serialize_food(food_item)), 200
            except ValidationError as e:
                return jsonify({"error_message": e.errors()}), 400
            except Exception:
                db.session.rollback()
                return jsonify({"error_message": "Unexpected error occurred"}), 500
        else:
            return jsonify({"error_message": "Permission denied"}), 403
        
@app.route('/api/meals', methods=['POST', 'GET'])
@jwt_required()
def create_get_meal():
    current_user_id = int(get_jwt_identity())
    if request.method == 'POST':
        try:
            user_meal = MealCreate(**request.get_json())
        except ValidationError as e:
            return jsonify({"error_message": e.errors()}), 400
        meal_name = user_meal.name
        query = sa.Select(Meal).where(and_(meal_name == Meal.name, Meal.user_id == current_user_id))
        result = db.session.scalar(query)
        if result:
            return jsonify({"error_message": f"'{meal_name}' already exists"}), 409
        is_saved = user_meal.saved
        meal_items = user_meal.food_items
        meal_food_list = []
        for meal_food in meal_items:
            food = db.session.get(Food, meal_food.food_id)
            if not food:
                return jsonify({"error_message": f"Food with id {meal_food.food_id} not found"}), 404
            if food.user_id != current_user_id or food.user_id is None:
                return jsonify({"error_message": "Permission denied"}), 403
            new_meal_food = Meal_Food(
                food_id=meal_food.food_id,
                quantity=meal_food.quantity
            )
            meal_food_list.append(new_meal_food)
        new_meal = Meal(
            name=meal_name,
            saved=is_saved,
            user_id=current_user_id,
            food_items=meal_food_list
        )
        try:
            date_time = datetime.now(timezone.utc).isoformat()
            db.session.add(new_meal)
            db.session.commit()
            return jsonify(serialize_meal_create(new_meal, date_time)), 201
        except Exception:
            db.session.rollback()
            return jsonify({"error_message": "Unexpected error occurred"}), 500

    if request.method == 'GET':
        try:
            meals_query = sa.select(Meal).where(Meal.user_id == current_user_id)
            meals = db.session.scalars(meals_query).all()  # List of Meal Response objects
            return [serialize_meal(meal) for meal in meals]
        except Exception:
            return jsonify({"error_message": "Unexpected error occurred"}), 500

@app.route('/api/meals/<int:meal_id>/foods', methods=['GET', 'POST', 'PATCH'])
@jwt_required()
def add_edit_meal(meal_id):
    # Either add a food to meal or edit existing foods of a meal or get list of foods in meal
    current_user_id = int(get_jwt_identity())
    meal = db.session.get(Meal, meal_id)
    if not meal:
        return jsonify({"error_message": "Meal not found"}), 404
    data = request.get_json()
    if "quantity" not in data:
        return jsonify({"error_message": "Missing required field"}), 422
    if request.method == 'POST':
        if "food_id" in data:  # format: {"food_id": ..., "quantity": ...}
            food = db.session.get(Food, data["food_id"])
            if not food:
                return jsonify({"error_message": f"Food with id {data["food_id"]} not found"}), 404
            try:
                user_new_food = MealFoodInput(**request.get_json())
            except ValidationError as e:
                return jsonify({"error_message": e.errors()}), 400
        elif "name" in data:  # format: just like creating a new food
            try:
                user_new_food = FoodCreateEdit(**request.get_json())
            except ValidationError as e:
                return jsonify({"error_message": e.errors()}), 400
            food = Food (
                name=user_new_food.name,
                calories=user_new_food.calories,
                protein=user_new_food.protein,
                carbs=user_new_food.carbs,
                fat=user_new_food.fat,
                serving_size=user_new_food.serving_size,
                serving_unit=user_new_food.serving_unit
            )
            db.session.add(food)
            db.session.flush()
        else:
            return jsonify({"error_message": "Must provide either food_id or food objects"}), 400
        
        quantity = data["quantity"]
        meal_food = Meal_Food(
            meal_id=meal.id,
            food_id=food.id,
            quantity=quantity
        )
        try:
            updated_at = datetime.now(timezone.utc).isoformat()
            db.session.add(meal_food)
            db.session.commit()
            return jsonify(serialize_meal_edit(meal, updated_at)), 201
        except Exception:
            db.session.rollback()
            return jsonify({"error_message": "Unexpected error occurred"}), 500

@app.route('/api/meals/<int:meal_id>', methods=['PUT', 'PATCH', 'DELETE'])
@jwt_required()
def up_rep_remove_meal(meal_id):
    # Either update, replace, or delete a meal
    current_user_id = int(get_jwt_identity())
    meal = db.session.get(Meal, meal_id)
    if request.method == 'DELETE':
        if meal.user_id == current_user_id:
            try:
                db.session.delete(meal)
                db.session.commit()
                return '', 204
            except Exception:
                db.session.rollback()
                return jsonify({"error_message": "Unexpected error occurred"}), 500
        else:
            return jsonify({"error_message": "Permission denied"}), 403

@app.route('/api/profile', methods=["PATCH"])
@jwt_required()
def update_user():
    user_data = request.get_json()
    print(f"receieved: {user_data}")
    username = user_data["username"]
    password = user_data["password"]  # NOTE: have not implemented hashing yet!!!!
    email_front_end = user_data["email"]
    email = email_front_end.lower()
    age = user_data.get("age")
    weight = user_data.get("weight")
    goal = user_data.get("goal")
    return

@app.route('/')
def test():
    return "Welcome to TrackingForMe, a macro-nutrient tracker to help you stay on track with your nutrition goals!"