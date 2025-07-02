"""
Module: main/routes.py
Description: Defines the home page route.
"""

from flask import Blueprint, render_template

main = Blueprint('main', __name__)

@main.route('/')
def home():
    """
    Render the homepage of the application.
    """
    return render_template("index.html")
