from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

#from flask_migrate import Migrate

from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

engine = create_engine("sqlite:///questions.db")
Base = declarative_base()

Base.metadata.bind = engine
Base.metadata.create_all()

Session = sessionmaker(bind=engine)
session = Session()

db=SQLAlchemy()

def create_app(config):
    app=Flask(__name__)

    app.config.from_object(config)

    db.init_app(app)
    
   # migrate = Migrate(app, db)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))
        
    from .auth import auth as auth_settings
    from .main import main as main_quizapp    
    
    app.register_blueprint(auth_settings)
    app.register_blueprint(main_quizapp)

    with app.app_context():
        db.create_all()

    return app

