from flask import Blueprint

main = Blueprint("main", __name__)

from quizproject.main import routes