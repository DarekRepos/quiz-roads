from flask import Blueprint

question_api = Blueprint("api", __name__)

from quizproject.api import api