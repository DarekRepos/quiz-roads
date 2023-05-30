from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from flask_wtf.csrf import CSRFProtect

# from flasgger import Swagger
from flask_session import Session


db = SQLAlchemy()


def create_app(config):
    app = Flask(__name__)

    app.config.from_object(config)
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

    from .auth import auth as auth_settings
    from .main import main as main_quizapp
    from .api import question_api as apis
    from .errors import bp as errors_bp
    from .commands.question_manager import bp as questions_cli

    app.register_blueprint(errors_bp)
    app.register_blueprint(auth_settings)
    app.register_blueprint(main_quizapp)
    app.register_blueprint(questions_cli)
    app.register_blueprint(apis)

    sess.init_app(app)

    with app.app_context():
        db.create_all()

    return app
