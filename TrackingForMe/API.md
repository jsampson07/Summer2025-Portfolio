3-5 "must-have" rsrcs
    1. User
        - id (integer primary key)
        - username
        - password (hashed)
        - email
        - age (int)
        - weight (float)
        - goal (enum: bulk, cut, maintenance, casual)
    2. Food (either stand-alone or makes up a meal w/ other foods)
        - id (lets include it so its just easier to read when making requests)
        - name (name can uniquely identify the food NO need for id)
        - calories
        - protein
        - carbs
        - fats
        restrictions:
            + ALL numeric vals MUST be ints (NO FLOATS!!! makes no sense)
        + I WANT food items to be saved to a user's account and can look up a food easily and add it to i.e. a meal
    3. Meal (collection of foods???)
        - id (lets include it so its just easier to read when making requests)
        - total_calories
        - total_protein
        - total_carbs
        - total_fats
        side note: *totals* ==> computed (derived attribute) NOT stored
        - saved (if the meal is saved so as to be displayed on the "Main Page 2 (Meal Catalog)" pg)
        a. foods: array of {food_name} w/ drill down to each of their respective nutritional info
            their information
    4. Summary
        - user_id
        - date
        - mode: enum(daily, weekly, monthly)
        - macro_breadown
            + BASED on the *mode* attribute ==> compute via aggregations (???)
        - weight_breakdown
            + BASED on the *mode* attribute ==> compute via all previous weights and date timeline and create a plot/linear progression line??

**API endpoints design**


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
        fats: ...
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

# we do not want users to be able to "upload" any new information to this page, it should all be derived from other pages of the application
- GET /api/summary
    # get the summary for this particular user