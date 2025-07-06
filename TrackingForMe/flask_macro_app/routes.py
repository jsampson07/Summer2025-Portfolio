# Define routes and handlers for the endpoints
from flask_macro_app import app
from flask import jsonify

@app.route('/api/foods')
def get_foods():
    ret_list = ["Chicken", "Bread", "Brown Rice", "Coke", "Steak", "Beef", "Mayonnaise", "Cashews"]
    return jsonify(ret_list) #wraps JSON output within Flask "Response" object -> sets Content-Type header auto to applicatin/json

@app.route('/')
def test():
    return "Welcome to TrackingForMe, a macro-nutrient tracker to help you stay on track with your nutrition goals!"