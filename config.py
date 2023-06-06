# -*- encoding: utf-8 -*-

import redis
import os
from dotenv import load_dotenv

load_dotenv()
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    """
    Base configuration class. Contains default configuration settings + configuration settings applicable to all environments.
    """

    # Default settings
    FLASK_ENV = "development"
    DEBUG = False
    TESTING = False
    WTF_CSRF_ENABLED = True
    WTF_CSRF_CHECK_DEFAULT = True

    # Settings applicable to all environments

    SECRET_KEY = os.getenv("SECRET_KEY", default="A very terrible secret key")
    CSRF_SECRET_KEY = os.getenv("CSRF_SECRET_KEY", default="A very terrible secret key")

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = "smtp.googlemail.com"
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.getenv("MAIL_USERNAME", default="")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD", default="")
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_USERNAME", default="")
    MAIL_SUPPRESS_SEND = False

    CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL ')
    RESULT_BACKEND = os.getenv('RESULT_BACKEND')
    
    #   Redis conf
    SESSION_TYPE = "redis"
    SESSION_PERMANENT = False
    SESSION_USE_SIGNER = True
    SESSION_REDIS = redis.from_url(os.getenv("SESSION_REDIS"))

    # Assets Management
    # ASSETS_ROOT = os.getenv('ASSETS_ROOT', '/static/otherfolder')


class DevelopmentConfig(Config):
    DEBUG = True
    PASSTHROUGH_ERRORS = True
    USE_DEBUGGER = True
    USE_RELOADER = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///dev.db"


class TestingConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False
    WTF_CSRF_CHECK_DEFAULT = False
    MAIL_SUPPRESS_SEND = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///testdatabase.db"


class ProductionConfig(Config):
    FLASK_ENV = "production"
    #   This will create a file in <app> FOLDER
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "PROD_DATABASE_URI", default="sqlite:///" + os.path.join(basedir, "prod.db")
    )
    # Security
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_DURATION = 3600
