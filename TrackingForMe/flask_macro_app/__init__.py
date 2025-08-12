from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enables CORS in Flask application
app.config.from_object(Config)

import click
from flask.cli import with_appcontext
@click.command('init-db')
@with_appcontext
def init_db():
    db.drop_all()
    db.create_all()
    click.echo("Database reinitialized confirmation")

jwt = JWTManager()
jwt.init_app(app)

# Create database instance for the application
db = SQLAlchemy(app)
# Create the migration engine instance to track db changes in application
migrate = Migrate(app, db)

from flask_macro_app.seed import seed_database, query_seed
app.cli.add_command(seed_database)
app.cli.add_command(query_seed)
app.cli.add_command(init_db)
from flask_macro_app import routes, models