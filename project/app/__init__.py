import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate
from config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
migrate = Migrate()

login_manager.login_view = 'auth.login'
login_manager.login_message = "You aren't logged in!"
login_manager.login_message_category = 'info'

UPLOAD_FOLDER = os.path.join('app', 'static', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    from app.auth.routes import auth
    from app.main.routes import main
    from app.survey.routes import survey
    from app.profile.routes import profile

    app.register_blueprint(auth)
    app.register_blueprint(main)
    app.register_blueprint(survey)
    app.register_blueprint(profile)

    # ✅ Automatically create tables on app start
    with app.app_context():
        from app.models import Upload  # 👈 Import your model(s)
        db.create_all()               # 👈 Create any missing tables

    return app
