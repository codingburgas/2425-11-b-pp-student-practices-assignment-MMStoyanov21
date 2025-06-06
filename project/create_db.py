from app import app, db
from app.models import User, Survey  # adjust import if needed

with app.app_context():
    db.create_all()
    print("Tables created!")
