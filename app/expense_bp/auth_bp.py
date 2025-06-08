from flask import Blueprint, flash, jsonify, render_template, redirect, url_for, request
from flask_security import login_required, current_user
from app.models.user import User
from extension import db





auth_bp = Blueprint('auth_bp', __name__, url_prefix='/auth')

# ----------------------
# Authentication Routes
# ----------------------

@auth_bp.route('/profile')
@login_required
def profile():
    """Display current user's profile"""
    return render_template('auth/profile.html', user=current_user)


@auth_bp.route('/users')
@login_required
def users():
    """View: List all users with optional search"""
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '', type=str)

    query = User.query

    if search:
        query = query.filter(
            (User.email.contains(search)) |
            (User.first_name.contains(search)) |
            (User.last_name.contains(search))
        )

    users = query.paginate(page=page, per_page=20, error_out=False)

    return render_template('auth/users.html',
                           users=users,
                           current_search=search)


@auth_bp.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    """Edit user details (no role logic included)"""
    user = User.query.get_or_404(user_id)

    if request.method == 'POST':
        user.first_name = request.form.get('first_name')
        user.last_name = request.form.get('last_name')
        user.phone = request.form.get('phone')
        user.active = 'active' in request.form

        try:
            db.session.commit()
            flash(f'User {user.email} updated successfully!', 'success')
            return redirect(url_for('auth_bp.users'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating user: {str(e)}', 'error')

    return render_template('auth/edit_user.html', user=user)


@auth_bp.route('/users/<int:user_id>/toggle-status', methods=['POST'])
@login_required
def toggle_user_status(user_id):
    """Toggle user's active status (AJAX support)"""
    user = User.query.get_or_404(user_id)

    if user.id == current_user.id:
        return jsonify({'error': 'You cannot deactivate your own account'}), 400

    user.active = not user.active
    db.session.commit()

    status = 'activated' if user.active else 'deactivated'
    return jsonify({'message': f'User {user.email} {status} successfully'})

