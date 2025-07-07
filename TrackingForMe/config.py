# Used to store configuration variables
# The "config" class is accessible by other moduless

import os
basedir = os.path.abspath(os.path.dirname(__file__))
# As we need more configuration *settings*, we can add ot this class
# We can access configuration variables w/ "dictionary syntax"
    # i.e. in Flask level module, app.config["SECRET_KEY"]
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or "default-secret-key-for-development"
    # location of application's database (where we are 'hosting' the database)
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or "sqlite:///" + os.path.join(basedir,
                                                                                           "app.db")
    