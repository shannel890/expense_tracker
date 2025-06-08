from extension import db
import uuid
from flask_login import UserMixin
from datetime import datetime
import pytz
from werkzeug.security import check_password_hash, generate_password_hash

KENYA_TIMEZONE = pytz.timezone('Africa/Nairobi')

def kenya_time():
    return datetime.now(KENYA_TIMEZONE)

class User(UserMixin,db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    phone = db.Column(db.String(20))
    active = db.Column(db.Boolean(), default=True)
    confirmed_at = db.Column(db.DateTime())
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    fs_uniquifier = db.Column(db.String(64), unique=True, nullable=True, default=lambda: str(uuid.uuid4()))
    last_login_at = db.Column(db.DateTime())
    current_login_at = db.Column(db.DateTime())
    last_login_ip = db.Column(db.String(45))
    current_login_ip = db.Column(db.String(45))
    login_count = db.Column(db.Integer, default=0)

    expenses = db.relationship('Expense', backref='user', lazy=True)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f'<User {self.username}>'