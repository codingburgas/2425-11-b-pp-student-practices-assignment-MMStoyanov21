from flask import Blueprint, render_template
from flask_login import current_user
from flask import session
main = Blueprint('main', __name__)

@main.route('/')
def home():
    if current_user.is_authenticated or session.get('is_admin'):
        # Show logged-in user or admin dashboard/homepage
        return render_template("dashboard.html")  # or your logged-in home page
    else:
        # Show public homepage
        return render_template("index.html")