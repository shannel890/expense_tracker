from flask import render_template
from app.models.category import Category
from flask_wtf import FlaskForm
from wtforms import (
    StringField, PasswordField, DecimalField,
    TextAreaField, SelectField, DateField,
    SubmitField, BooleanField
)
from wtforms.validators import DataRequired, Length, NumberRange, Optional
from datetime import date

# ========================
# User Authentication Forms
# ========================

class RegistrationForm(FlaskForm):
    """Form for user registration"""
    username = StringField(
        'Username',
        validators=[
            DataRequired('Username is required'),
            Length(min=3, max=64, message='Username must be between 3 and 64 characters')
        ]
    )
    email = StringField(
        'Email',
        validators=[
            DataRequired('Email is required'),
            Length(max=120, message='Email must be less than 120 characters')
        ]
    )
    password = PasswordField(
        'Password',
        validators=[
            DataRequired('Password is required'),
            Length(min=6, message='Password must be at least 6 characters long')
        ]
    )
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    """Form for user login"""
    email = StringField(
        'Email',
        validators=[DataRequired('Email is required')]
    )
    password = PasswordField(
        'Password',
        validators=[DataRequired('Password is required')]
    )
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


# ========================
# Expense Management Forms
# ========================

class ExpenseForm(FlaskForm):
    """Form for adding or editing an expense"""
    amount = DecimalField(
        'Amount (KES)',
        places=2,
        validators=[
            DataRequired('Amount is required'),
            NumberRange(min=0.01, message='Amount must be greater than zero')
        ]
    )
    category_id = SelectField(
        'Category',
        coerce=int,
        validators=[DataRequired('Please select a category')]
    )
    note = TextAreaField(
        'Note (Optional)',
        validators=[Optional()],
        render_kw={"rows": 3, "placeholder": "Add a note about this expense..."}
    )
    date = DateField(
        'Date',
        default=date.today,
        validators=[DataRequired('Please select a date')]
    )
    submit = SubmitField('Save Expense')


# ========================
# Reporting & Filter Form 
# ========================

class ReportFilterForm(FlaskForm):
    """Form for filtering expense reports"""
    start_date = DateField('Start Date', validators=[Optional()])
    end_date = DateField('End Date', validators=[Optional()])
    category_id = SelectField(
        'Category',
        coerce=int,
        validators=[Optional()]
    )
    export_csv = BooleanField('Export as CSV')
    submit = SubmitField('Apply Filter')


class DeleteExpenseForm(FlaskForm):
    """Form for confirming expense deletion"""
    confirm = BooleanField(
        'Are you sure you want to delete this expense?',
        validators=[DataRequired('Please confirm deletion')]
    )
    submit = SubmitField('Delete Expense')

