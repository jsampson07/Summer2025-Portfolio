# MacroTracker – Full Stack Nutrition App

MacroTracker is a full-stack web application that helps users log meals, track calories and macronutrients, and view progress summaries.  
It’s built with a **Flask backend** and a **React frontend**, showcasing full-stack skills in authentication, API design, database management, and user interface development.  

---

## Features
- **User Authentication:** Secure login and registration with JWT  
- **Meal & Food Management:** CRUD APIs for tracking meals and foods  
- **Database Management:** SQLAlchemy models with Flask-Migrate migrations  

---

## Tech Stack
**Backend**
- Python, Flask  
- SQLAlchemy, Flask-Migrate  
- JWT Authentication  

**Frontend**
- React  
- CSS Modules (styling)  

---

## Project Structure
MacroTracker/
├── backend/ # Flask REST API
├── frontend/ # React user interface
└── README.md # Project overview (this file)


---

## Getting Started

### Backend Setup
```bash
cd backend

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run database migrations
flask db upgrade

# Start the backend server
flask run
```

### Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Start the development server
npm start
```
