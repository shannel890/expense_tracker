from flask import Blueprint, flash, jsonify, render_template, redirect, url_for, request
from flask_security import login_required, current_user
from app.models.expense import Expense  # Hypothetical models
from app.models.category import Category
from app.models.expense import ExpenseType
from app.models.user import User

from extension import db

expense_bp = Blueprint('expense_bp', __name__, url_prefix='/expenses')

# ----------------------
# Expense Tracker Routes
# ----------------------

@expense_bp.route('/')
@login_required
def dashboard():
    """Dashboard for expense tracker"""
    return render_template('expense/dashboard.html')


@expense_bp.route('/list')
@login_required
def list_expenses():
    """List all expenses for the current user"""
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '', type=str)
    category_filter = request.args.get('category', '', type=str)

    query = Expense.query.filter_by(user_id=current_user.id)

    if search:
        query = query.filter(Expense.description.contains(search))

    if category_filter:
        query = query.filter_by(category_id=category_filter)

    expenses = query.paginate(page=page, per_page=20, error_out=False)

    categories = Category.query.all()

    return render_template('expense/list_expenses.html',
                           expenses=expenses,
                           categories=categories,
                           current_search=search,
                           current_category=category_filter)


@expense_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_expense():
    """Add a new expense"""
    if request.method == 'POST':
        description = request.form.get('description')
        amount = float(request.form.get('amount'))
        category_id = request.form.get('category_id')
        expense_type_id = request.form.get('expense_type_id')

        new_expense = Expense(
            user_id=current_user.id,
            description=description,
            amount=amount,
            category_id=category_id,
            expense_type_id=expense_type_id
        )

        try:
            db.session.add(new_expense)
            db.session.commit()
            flash('Expense added successfully!', 'success')
            return redirect(url_for('expense_bp.list_expenses'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding expense: {str(e)}', 'error')

    categories = Category.query.all()
    expense_types = ExpenseType.query.all()
    return render_template('expense/add_expense.html',
                           categories=categories,
                           expense_types=expense_types)


@expense_bp.route('/<int:expense_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_expense(expense_id):
    """Edit an existing expense"""
    expense = Expense.query.filter_by(id=expense_id, user_id=current_user.id).first_or_404()

    if request.method == 'POST':
        expense.description = request.form.get('description')
        expense.amount = float(request.form.get('amount'))
        expense.category_id = request.form.get('category_id')
        expense.expense_type_id = request.form.get('expense_type_id')

        try:
            db.session.commit()
            flash('Expense updated successfully!', 'success')
            return redirect(url_for('expense_bp.list_expenses'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating expense: {str(e)}', 'error')

    categories = Category.query.all()
    expense_types = ExpenseType.query.all()
    return render_template('expense/edit_expense.html',
                           expense=expense,
                           categories=categories,
                           expense_types=expense_types)


@expense_bp.route('/categories/by-type/<int:type_id>')
@login_required
def categories_by_type(type_id):
    """Get categories by expense type (AJAX endpoint)"""
    categories = Category.query.filter_by(expense_type_id=type_id, active=True).all()
    return jsonify([{'id': cat.id, 'name': cat.name} for cat in categories])


@expense_bp.route('/report')
@login_required
def expense_report():
    """Generate expense report"""
    return render_template('expense/report.html')


# -----------------------
# Moved Auth/User Routes
# -----------------------
# These can be moved to auth_bp.py or admin_bp.py