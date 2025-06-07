import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate
from config import Config

# Initialize extensions
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
migrate = Migrate()

# Set login view and message
login_manager.login_view = 'auth.login'
login_manager.login_message = "You aren't logged in!"
login_manager.login_message_category = 'info'

# Path for uploaded CSVs
UPLOAD_FOLDER = os.path.join('app', 'static', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Create if it doesn't exist

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Upload folder config
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    # Register Blueprints
    from app.auth.routes import auth
    from app.main.routes import main
    from app.survey.routes import survey

    app.register_blueprint(auth)
    app.register_blueprint(main)
    app.register_blueprint(survey)

    return app
