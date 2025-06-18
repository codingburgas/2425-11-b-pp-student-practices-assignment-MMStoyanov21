from flask import Blueprint, render_template, redirect, url_for, flash, session
from flask_login import login_required, current_user
from app.models import User, db

dashboard = Blueprint('dashboard', __name__)

@dashboard.route("/dashboard")
def admin_dashboard():
    # Allow access to real admin users or session admin
    if not (session.get('is_admin') or (current_user.is_authenticated and current_user.role == 'admin')):
        flash("Access denied.", "danger")
        return redirect(url_for('main.home'))

    users = User.query.all()
    return render_template("dashboard.html", users=users)

@dashboard.route("/delete_user/<int:user_id>")
def delete_user(user_id):
    if not (session.get('is_admin') or (current_user.is_authenticated and current_user.role == 'admin')):
        flash("Unauthorized action.", "danger")
        return redirect(url_for('main.home'))

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash("User deleted.", "success")
    return redirect(url_for('dashboard.admin_dashboard'))
