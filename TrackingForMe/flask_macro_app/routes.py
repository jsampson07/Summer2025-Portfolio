# Define routes and handlers for the endpoints
from flask_macro_app import app
from flask import jsonify, request
from typing import List, Dict, Any
FOODS = [
    {"id": 1, "name": "Chicken", "calories": 200},
    {"id": 2, "name": "Whole Wheat Bread", "calories": 70},
    {"id": 4, "name": "Greek Yogurt", "calories": 170},
    {"id": 5, "name": "Egg Whites", "calories": 50},
    {"id": 3, "name": "Flavored-Pistachios", "calories": 100},
    {"id": 6, "name": "Cashews", "calories": 80}
]

def merge_sort(arr: List[Dict[str, Any]], sort_by):
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
    to_sort = request.args.get("sort")  # .args is a MultiDict of all query params i.e.
    sort_by = request.args.get("sort_by")  # Perhaps what to sort_by i.e. calories, protein, etc
        #http://www.example.com/api/foods?sort=merge -> to_sort = {"sort": "merge"}["sort"] == "merge"
    if to_sort == "merge":
        merge_sort(FOODS, sort_by)
        return jsonify(FOODS)
        # Sort given the FOODS list for now
    return jsonify(FOODS) #wraps JSON output within Flask "Response" object -> sets Content-Type header auto to applicatin/json

@app.route('/')
def test():
    return "Welcome to TrackingForMe, a macro-nutrient tracker to help you stay on track with your nutrition goals!"