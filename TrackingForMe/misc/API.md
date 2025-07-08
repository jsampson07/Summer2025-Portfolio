**API endpointegers design**


/api/users/* 

*POST*
- POST /api/register -> create a user                ==> WHY THESE TWO??? BECAUSE while we
- POST /api/login -> authenticate (returns a token)  ==> can have it in /users, separates jobs
- GET /api/users/{id} -> read profile for user with user_id **OR** /api/users/me
- PUT /api/users/{id} -> replace entire user profile
- PATCH /api/users/{id} -> update part of user's profile (i.e. weight, goal)
- DELETE /api/users/{id} -> remove a users account and all their respective data


/api/foods/*

- POST /api/foods --> create a new food item
    body = {
        name: ...,
        calories: ...,
        protein: ...,
        carbs: ...,
        fat: ...
    }
- GET /api/foods --> retrieval a list of all foods the user has
    + support query parameters like ?sort=merge OR ?name={food_name}
        **what is ?sort=merge**????
- GET /api/foods/{food_id} --> retrieve nutritional info on a food
- PATCH /api/foods/{food_id} --> edit particular info of a food (protein, calories, etc)
    + i.e. { protein: 40 }
- DELETE /api/foods/{food_id} --> remove a food from user's "catalog"


/api/meals/*

- POST /api/meals --> create a new meal (with food(s) in it)

- POST /api/meals/{meal_id}/foods --> add a food to a meal
    ==> this also adds to the foods collection as a whole too
    **OR**
- PATCH /api/meals/{meal_id} --> add/remove a food to a meal (just update the "foods" array in some way) OR just "partially" update a meal i.e. its "saved" flag (whether user wants it saved or not)
    ==> do this by having a "+" button that users can press for each meal

- GET /api/meals --> get list of every meal they have to be able to pick from previous meals
    + support *paging*
- GET /api/meals/{meal_id} --> get list of all of foods in a particular meal
    + embeds the foods array in the response with the meal request
- PUT /api/meals/{meal_id} --> update/replace entire meal
- DELETE /api/meals/{meal_id} --> remove a meal


/api/summary/*

*we do not want users to be able to "upload" any new information to this page, it should all be derived from other pages of the application*
- GET /api/summary
    *get the summary for this particular user*
    *use ?date={date}&mode={mode} to display SummaryResponse*

**JSON schema for "client requests" and "server responses"**
*User*
UserInput:
{
    "type": "object",
    "properties": {
        "username": {"type": "string"},
        "password": {"type": "string"},
        "email": {"type": "string", "format": "email"},
        "age": {"type": "integer"},
        "weight": {"type": "number"},
        "goal": {
            "type": "string",
            "enum": ["casual", "cut", "bulk", "maintain"]
        }
    },
    "required": ["username", "password", "email"]
}
PartialUserInput:
{
    "type": "object",
    "properties": {
        "username": {"type": "string"},
        "password": {"type": "string"},
        "email": {"type": "string", "format": "email"},
        "age": {"type": "integer"},
        "weight": {"type": "number"},
        "goal": {
            "type": "string",
            "enum": ["casual", "cut", "bulk", "maintain"]
        }
    }
}
UserResponse:
{
    "type": "object",
    "properties": {
        "id": {"type": "integer"},
        "username": {"type": "string"},
        "email": {"type": "string"},
        "age": {"type": "integer"},
        "weight": {"type": "number"},
        "goal": {
            "type": "string",
            "enum": ["casual", "cut", "bulk", "maintain"]
        },
        "created_at": {"type": "string", "format": "date-time"},
        "updated_at": {"type": "string", "format": "date-time"}
    },
    "required": ["id", "username", "email"]
}

*Food*
FoodInput:
{
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "serving_size": {"type": "number"},
        "serving_unit": {"type": "string", "enum": ["g", "oz", "mL", "cup", "unit"]},
        "calories": {"type": "integer"},
        "protein": {"type": "integer"},
        "carbs": {"type": "integer"},
        "fat": {"type": "integer"}
    },
    "required": ["name", "serving_size", "serving_unit", "calories"]
}
PartialFoodInput:
{
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "serving_size": {"type": "number"},
        "serving_unit": {"type": "string", "enum": ["g", "oz", "mL", "cup", "unit"]},
        "calories": {"type": "integer"},
        "protein": {"type": "integer"},
        "carbs": {"type": "integer"},
        "fat": {"type": "integer"}
    }
}
FoodResponse:
{
    "type": "object",
    "properties": {
        "id": {"type": "integer"},
        "name": {"type": "string"},
        "serving_size": {"type": "number"},
        "serving_unit": {"type": "string", "enum": ["g", "oz", "mL", "cup", "unit"]},
        "calories": {"type": "integer"},
        "protein": {"type": "integer"},
        "carbs": {"type": "integer"},
        "fat": {"type": "integer"},
        "created_at": {"type": "string", "format": "date-time"},
        "updated_at": {"type": "string", "format": "date-time"}
    },
    "required": ["id", "name", "serving_size", "serving_unit", "calories"]
}

*Meal*
MealInput:
{
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "saved": {"type": "boolean"},
        "foods": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "food_id": {"type": "integer"},
                    "quantity": {"type": "number"}
                },
                "required": ["food_id", "quantity"]
            }
        }
    },
    "required": ["name", "foods"]
}
PartialMealInput:
{
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "saved": {"type": "boolean"},
        "foods": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "food_id": {"type": "integer"},
                    "quantity": {"type": "number"}
                },
                "required": ["food_id", "quantity"]
            }
        }
    }
}
MealResponse:
{
    "type": "object",
    "properties": {
        "id": {"type": "integer"},
        "name": {"type": "string"},
        "total_calories": {"type": "integer"},
        "total_protein": {"type": "integer"},
        "total_carbs": {"type": "integer"},
        "total_fat": {"type": "integer"},
        "saved": {"type": "boolean"},
        "foods": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "quantity": {"type": "number"}
                    "food": {
                        "type": "object",
                        "properties": {
                            "food_id": {"type": "integer"},
                            "serving_size": {"type": "number"},
                            "serving_unit": {"type": "string"},
                            "name": {"type": "string"},
                            "calories": {"type": "integer"},
                            "protein": {"type": "integer"},
                            "carbs": {"type": "integer"},
                            "fat": {"type": "integer"}
                        },
                        "required": ["id", "name", "serving_size", "serving_unit", "calories"]
                    }
                },
                "required": ["quantity, "food"]
            }
        },
        "created_at": {"type": "string", "format": "date-time"},
        "updated_at": {"type": "string", "format": "date-time"}
    },
    "required": ["id", "name", "total_calories", "saved", "foods"]
}

*Summary*
SummaryResponse:
{
    "type": "object",
    "properties": {
        "date": {"type": "string", "format": "date"},
        "mode": {
            "type": "string",
            "enum": ["daily", "weekly", "monthly"]
        },
        "macro_breakdown": {
            "type": "object",
            "properties": {
                "avg_calories": {"type": "number"},
                "avg_protein": {"type": "number"},
                "avg_carbs": {"type": "number"},
                "avg_fat": {"type": "number"}
            },
            "required": ["avg_calories"]
        },
        "weight_breakdown": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "date": {"type": "string", "format": "date"},
                    "weight": {"type": "number"}
                },
                "required": ["weight"]
            }
        },
        "created_at": {"type": "string", "format": "date-time"},
        "updated_at": {"type": "string", "format": "date-time"}
    },
    "required": ["date", "mode", "macro_breakdown"]
}

*Daily_Log*
DailyLogInput:
{
    "type": "object",
    "properties": {
        "log_date": {"type": "string", "format": "date-time"},
        "quantity": {"type": "number"},
        "food_id": {"type": "integer},
        "meal_id": {"type": "integer"},
    },
    "required": ["log_date", "quantity"],
    "oneOf": [
        {"required": ["food_id"]},
        {"required": ["meal_id"]}
    ]
}
DailyLogResponse:
{
    "type": "object",
    "properties": {
        "date": {"type": "string", "format": "date"},
        "daily_totals": {
            "type": "object",
            "properties": {
                "calories": {"type": "integer"},
                "protein": {"type": "integer"},
                "carbs": {"type": "integer"},
                "fat": {"type": "integer"}
            }
        }
        "log_entries": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "log_id": {"type": "integer"},
                    "food_meal_name": {"type": "string"},
                    "quantity": {"type": "integer"},
                    "calories": {"type": "integer"},
                    "protein": {"type": "integer"},
                    "carbs": {"type": "integer"},
                    "fat": {"type": "integer}
                },
                "required": ["log_id", "food_meal_name", "calories"]
            }
        }
        "created_at": {"type": "date", "format": "date"},
        "updated_at": {"type": "date", "format": "date"}
    },
    "required": ["date", "daily_totals", "log_entries", "created_at"]
}