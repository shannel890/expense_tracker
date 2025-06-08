from extension import db
from flask_login import UserMixin
from datetime import datetime
import pytz

KENYA_TIMEZONE = pytz.timezone('Africa/Nairobi')

def kenya_time():
    return datetime.now(KENYA_TIMEZONE)

class Expense(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float(precision=2), nullable=False)
    note = db.Column(db.String(255))
    date = db.Column(db.DateTime, default=kenya_time, nullable=False)
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    category = db.relationship('Category', back_populates='expenses')

    def __repr__(self):
        return f'<Expense {self.amount} on {self.date}>'
    
class ExpenseType(db.Model):
    __tablename__ = 'expense_types'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)