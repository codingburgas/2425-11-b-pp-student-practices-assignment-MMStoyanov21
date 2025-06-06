from datetime import datetime
from flask_login import UserMixin
from app import db
from app import login_manager

# Flask-Login user loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='student')
    confirmed = db.Column(db.Boolean, default=False)

    # Relationship: One user has many surveys
    surveys = db.relationship('Survey', backref='author', lazy=True)

    def __repr__(self):
        return (
            f"<User(username='{self.username}', email='{self.email}', "
            f"role='{self.role}', confirmed={self.confirmed})>"
        )


class Survey(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hours_studied = db.Column(db.Float, nullable=False)
    predicted_score = db.Column(db.Float, nullable=True)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return (
            f"<Survey(user_id={self.user_id}, hours_studied={self.hours_studied}, "
            f"predicted_score={self.predicted_score})>"
        )
