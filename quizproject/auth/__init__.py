from flask import Blueprint

bp = Blueprint("auth", __name__)

from quizproject.auth import routes