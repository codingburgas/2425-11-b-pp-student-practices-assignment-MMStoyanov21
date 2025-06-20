from flask import Blueprint, render_template
from flask_login import current_user
from flask import session
main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template("index.html")