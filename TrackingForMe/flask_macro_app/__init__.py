from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config.from_object(Config)

jwt = JWTManager()

# Create database instance for the application
db = SQLAlchemy(app)
# Create the migration engine instance to track db changes in application
migrate = Migrate(app, db)

from flask_macro_app.seed import seed_database, query_seed
app.cli.add_command(seed_database)
app.cli.add_command(query_seed)
from flask_macro_app import routes, models