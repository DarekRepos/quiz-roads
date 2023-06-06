import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from flask_wtf.csrf import CSRFProtect

# from flasgger import Swagger
from flask_session import Session
from celery import Celery
from config import Config

db = SQLAlchemy()

### Flask extension objects instantiation ###
mail = Mail()

### Instantiate Celery ###
celery = Celery(
    __name__, broker=Config.CELERY_BROKER_URL, result_backend=Config.RESULT_BACKEND
)


def create_app():
    app = Flask(__name__)

    CONFIG_TYPE = os.getenv("CONFIG_TYPE", default="config.DevelopmentConfig")
    app.config.from_object(CONFIG_TYPE)
    # Configure celery
    celery.conf.update(app.config)

    #  swagger = Swagger(app, config=config)
    sess = Session(app)

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    from .models.users import User

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table,
        # use it in the query for the user
        return User.query.filter_by(user_id=user_id).first()

    csrf = CSRFProtect()
    csrf.init_app(app)

    register_blueprints(app)

    sess.init_app(app)

    with app.app_context():
        db.create_all()

    configure_logging(app)

    return app


## Helper function


def register_blueprints(app):
    from .auth import auth as auth_settings
    from .main import main as main_quizapp
    from .api import question_api as apis
    from .errors import bp as errors_handlers
    from .commands.question_manager import bp as questions_cli

    app.register_blueprint(errors_handlers)
    app.register_blueprint(auth_settings)
    app.register_blueprint(main_quizapp)
    app.register_blueprint(questions_cli)
    app.register_blueprint(apis)


def configure_logging(app):
    import logging
    from flask.logging import default_handler
    from logging.handlers import RotatingFileHandler

    # Deactivate the default flask logger so that log messages don't get duplicated
    app.logger.removeHandler(default_handler)

    # Create a file handler object
    file_handler = RotatingFileHandler("flaskapp.log", maxBytes=16384, backupCount=20)

    # Set the logging level of the file handler object so that it logs INFO and up
    file_handler.setLevel(logging.INFO)

    # Create a file formatter object
    file_formatter = logging.Formatter(
        "%(asctime)s %(levelname)s: %(message)s [in %(filename)s: %(lineno)d]"
    )

    # Apply the file formatter object to the file handler object
    file_handler.setFormatter(file_formatter)

    # Add file handler object to the logger
    app.logger.addHandler(file_handler)
