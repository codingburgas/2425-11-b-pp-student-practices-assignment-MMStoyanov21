from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate
from config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = "You aren't logged in!"
login_manager.login_message_category = 'info'
migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    from app.auth.routes import auth
    app.register_blueprint(auth)

    from app.main.routes import main
    app.register_blueprint(main)

    from app.survey.routes import survey
    app.register_blueprint(survey)

    # 🔧 Create tables if they don't exist
    with app.app_context():
        from app import models  # Ensure models are loaded
        db.create_all()

    return app
