# Define routes and handlers for the endpoints
from flask_macro_app import app, db
from flask_macro_app.models import User, Food
from flask import jsonify, request
from typing import List, Dict, Any
import sqlalchemy as sa

def merge_sort(arr: List[Dict[str, Any]]):
    """Used to sort 'foods' by calories; later add feature to sort by desired filter"""
    # Base cases
    if len(arr) == 1:
        return
    # Create sub-arrs
    length = len(arr)
    midIndex = int(length/2)
    left = arr[0:midIndex]
    right = arr[midIndex:]
    merge_sort(left)
    merge_sort(right)

    i,j = 0,0
    # We want it to iterate until we are at the end of one of the arrays
    while ((i < len(left)) and (j < len(right))):
        if left[i]["calories"] <= right[j]["calories"]:
            arr[i+j] = left[i]
            i+=1
        else:
            arr[i+j] = right[j]
            j+=1
    # Iterate through "incomplete" array
    while i < len(left):
        arr[i+j] = left[i]
        i+=1
    while j < len(right):
        arr[i+j] = right[j]
        j+=1

@app.route('/api/foods')
def get_foods():
    query = sa.select(Food)
    foods = db.session.scalars(query).all()
    to_sort = request.args.get("sort")  # .args is a MultiDict of all query params i.e.
    #sort_by = request.args.get("sort_by")  # Perhaps what to sort_by i.e. calories, protein, etc
        #http://www.example.com/api/foods?sort=merge -> to_sort = {"sort": "merge"}["sort"] == "merge"
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
    if to_sort == "merge":
        merge_sort(new_foods_list)
        return jsonify(new_foods_list)
        # Sort given the FOODS list for now
    return jsonify(new_foods_list) #wraps JSON output within Flask "Response" object -> sets Content-Type header auto to applicatin/json

@app.route('/api/register', methods=['POST'])
def create_user():
    print("Creating user...")

    

    print("Successfully created user!")

@app.route('/')
def test():
    return "Welcome to TrackingForMe, a macro-nutrient tracker to help you stay on track with your nutrition goals!"