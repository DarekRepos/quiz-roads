from flask import Blueprint

bp = Blueprint("errors", __name__)

from quizproject.errors import handlers
