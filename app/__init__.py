from flask import Flask
from extension import db
from config import Config





def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    
    db.init_app(app)

    with app.app_context():
        # ✅ Import all models so SQLAlchemy knows them
        from app.models.expense import Expense, ExpenseType
        from app.models.category import Category
        from app.models.user import User  # if needed

        # If you're using Flask-Migrate, do NOT call create_all()
        db.create_all()  # or run migrations

    return app

    
    
    
