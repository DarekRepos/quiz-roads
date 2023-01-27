from flask import Blueprint, render_template
from flask_login import login_required, current_user

main = Blueprint('main', __name__)


@main.route("/")
def index():
    return render_template('index.html')


@main.route("/profile")
@login_required
def profile():
    return render_template('profile.html', name=current_user.user_name)


@main.route("/quiz")
@login_required
def quiz():
    return render_template('quiz.html')
