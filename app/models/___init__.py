# app/models/__init__.py
from .category import Category
from extension import db
# You can also import other models here if needed
def seed_categories():
    categories = [
        "Food", "Transport", "Housing", "Education", "Health",
        "Entertainment", "Shopping", "Bills", "Savings", "Other"
    ]
    for name in categories:
        if not Category.query.filter_by(name=name).first():
            db.session.add(Category(name=name))
    db.session.commit()