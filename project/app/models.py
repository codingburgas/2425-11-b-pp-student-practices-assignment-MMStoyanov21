"""
Module: models.py
Description: Database models for users, uploads, surveys, estimations, and feedback.
"""

from datetime import datetime
from flask_login import UserMixin
from app import db, login_manager

@login_manager.user_loader
def load_user(user_id):
    """
    Load a user by ID for Flask-Login.
    """
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    """
    User model with authentication credentials and relationships.
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='student')
    confirmed = db.Column(db.Boolean, default=False)

    surveys = db.relationship('Survey', backref='author', lazy=True, cascade='all, delete-orphan')
    uploads = db.relationship('Upload', backref='user', lazy=True, cascade='all, delete-orphan')
    estimations = db.relationship('Estimation', backref='user', lazy=True, cascade='all, delete-orphan')
    feedbacks = db.relationship('Feedback', backref='author', lazy=True, cascade='all, delete-orphan')

class Survey(db.Model):
    """
    Stores survey outcomes and predicted scores.
    """
    id = db.Column(db.Integer, primary_key=True)
    hours_studied = db.Column(db.Float, nullable=False)
    predicted_score = db.Column(db.Float, nullable=True)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Upload(db.Model):
    """
    Represents uploaded files by users.
    """
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(120), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'<Upload {self.filename}>'

class Estimation(db.Model):
    """
    Textual estimation results linked to a user.
    """
    id = db.Column(db.Integer, primary_key=True)
    result = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Feedback(db.Model):
    """
    User-submitted feedback messages.
    """
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'<Feedback {self.subject}>'
