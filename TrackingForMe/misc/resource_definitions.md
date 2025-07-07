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
        - serving_size (i.e. 1, 1.5) - **RIGHT NOW NOT REQUIRED, default to multiple everything by 1**
        - serving_unit (i.e. cup, oz, mL, etc) **RIGHT NOW NOT REQUIRED treat all as 'unit'**
        - calories
        - protein
        - carbs
        - fats
        - user_id (foreign key) ==> user can create custom food items with their own nutritional info
            ==> new row is created in the Food table
                ==> user_id is set to user's ID that created it
            - by default user_id is NULL for "master catalog" where all users can see the 'dropdown' of prebuilt-in foods
        restrictions:
            + ALL numeric vals MUST be ints (NO FLOATS!!! makes no sense)
        + I WANT food items to be saved to a user's account and can look up a food easily and add it to i.e. a meal
    3. Meal (collection of foods???)
        - id (lets include it so its just easier to read when making requests)
        - name (can name a meal to make recognizable)
        - total_calories **ALL OF THESE ARE GOING TO BE DERIVED IN DB**
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
    5. Daily Log
        - id - uniquely identify each log entry
        - **log_date** ==> when the meal or food was consumed (so that we can use for summaries, how much did i eat today, this week, etc)
        - user_id
        - food_id (optional b/c both food and meal can be added to log)
        - meal_id (optional b/c both food and meal can be added to log)
        - quantity (NOT the same as the other "quantity" vals)
            ==> how much of this *food* or *meal* did I eat in this particular instance?