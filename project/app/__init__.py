from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from config import Config

from flask_bootstrap import Bootstrap
from flask_wtf.csrf import CSRFProtect


bcrypt = Bcrypt()
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'
mail = Mail()
migrate = Migrate()
bootstrap = Bootstrap()
csrf = CSRFProtect()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)
    bootstrap.init_app(app)
    csrf.init_app(app)

    from app.auth.routes import auth
    from app.main.routes import main
    from app.survey.routes import survey
    from app.dashboard.routes import dashboard

    app.register_blueprint(auth)
    app.register_blueprint(main)
    app.register_blueprint(survey)
    app.register_blueprint(dashboard)

    from app.main.errors import register_error_handlers
    register_error_handlers(app)

    return app