# -*- encoding: utf-8 -*-

import os

class Config(object):
    basedir = os.path.abspath(os.path.dirname(__file__))

    SECRET_KEY = os.getenv('SECRET_KEY')

    CSRF_SECRET_KEY = os.getenv('CSRF_SECRET_KEY')

       # This will create a file in <app> FOLDER
    SQLALCHEMY_DATABASE_URI = 'sqlite:///questions.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False 

    # Assets Management
    #ASSETS_ROOT = os.getenv('ASSETS_ROOT', '/static/otherfolder')    
    
class ProductionConfig(Config):
    DEBUG = False

    # Security
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_DURATION = 3600

class DebugConfig(Config):
    DEBUG = True


# Load all possible configurations
config_dict = {
    'Production': ProductionConfig,
    'Debug'     : DebugConfig
}