from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from flask_wtf.csrf import CSRFProtect

engine = create_engine("sqlite:///questions.db")
Base = declarative_base()

Base.metadata.bind = engine
Base.metadata.create_all()

Session = sessionmaker(bind=engine)
session = Session()

db = SQLAlchemy()


def token_error(e):
    return render_template('page-400.html'), 400


def access_forbidden(e):
    return render_template('page-403.html'), 403


def page_not_found(e):
    return render_template('page-404.html'), 404


def internal_error(e):
    return render_template('page-500.html'), 500


def create_app(config):
    app = Flask(__name__)

    app.config.from_object(config)

    app.register_error_handler(400, token_error)
    app.register_error_handler(403, access_forbidden)
    app.register_error_handler(404, page_not_found)
    app.register_error_handler(500, internal_error)

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table,
        # use it in the query for the user
        return User.query.get(int(user_id))

    csrf = CSRFProtect()
    csrf.init_app(app)

    from .auth import auth as auth_settings
    from .main import main as main_quizapp

    app.register_blueprint(auth_settings)
    app.register_blueprint(main_quizapp)

    with app.app_context():
        db.create_all()

    return app
