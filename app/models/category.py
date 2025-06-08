from extension import db
from flask_login import UserMixin
from datetime import datetime
import pytz

KENYA_TIMEZONE = pytz.timezone('Africa/Nairobi')

# Helper function to get current time in Kenya
def kenya_time():
    return datetime.now(KENYA_TIMEZONE)

class Category(UserMixin, db.Model):

    __tablename__ = 'category'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship to Expense model
    expenses = db.relationship('Expense', back_populates='category', lazy=True)

    def __repr__(self):
        return f"<Category {self.name}>"

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }