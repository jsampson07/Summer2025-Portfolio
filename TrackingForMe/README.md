Flask backend service for **my-macros-app**, a full-stack nutrition tracker that helps users log meals, track calories and macronutrients, and view progress summaries.

## Features
- User authentication with JWT
- Food and meal management (CRUD APIs)
- Nutrition API integration for calorie/macro lookup
- Database schema management with SQLAlchemy + Flask-Migrate

## Tech Stack
- Python, Flask
- SQLAlchemy, Flask-Migrate
- PostgreSQL
- JWT authentication

## Setup

```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run database migrations
flask db upgrade

# Start the backend server
flask run
