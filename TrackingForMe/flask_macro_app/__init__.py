from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)

# Create database instance for the application
db = SQLAlchemy(app)
# Create the migration engine instance to track db changes in application
migrate = Migrate(app, db)

from flask_macro_app import routes, models