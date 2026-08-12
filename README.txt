EXPENSE TRACKER - FLASK + BLUEPRINT + SQLALCHEMY

Features:
1. Signup
2. Login
3. Logout
4. Add expense
5. View expenses
6. Update expense
7. Delete expense
8. Total expense calculation
9. Category-wise expense summary
10. SQLite database
11. User-specific expenses
12. Password hashing
13. Blueprint architecture
14. SQLAlchemy ORM

SETUP:

1. Open this project folder in VS Code.

2. Open terminal in the folder containing run.py and requirements.txt.

3. Install packages:
   py -m pip install -r requirements.txt

4. Run:
   py run.py

5. Open:
   http://127.0.0.1:5000/

IMPORTANT:
The SQLite database is created automatically inside:
app/instance/expenses.db

If you want a completely fresh database, stop Flask and delete:
app/instance/expenses.db

PROJECT STRUCTURE:

expense_tracker_flask_project/
|-- run.py
|-- requirements.txt
|-- README.txt
|-- app/
    |-- __init__.py
    |-- models.py
    |-- auth/
    |   |-- __init__.py
    |   |-- routes.py
    |-- expenses/
    |   |-- __init__.py
    |   |-- routes.py
    |-- templates/
    |   |-- base.html
    |   |-- login.html
    |   |-- signup.html
    |   |-- index.html
    |   |-- add.html
    |   |-- update.html
    |-- static/
        |-- style.css
