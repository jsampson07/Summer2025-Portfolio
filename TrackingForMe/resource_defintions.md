**Resources for Application**
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
        - name (can name a meal to make recognizable)
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