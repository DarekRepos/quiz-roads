from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from sqlalchemy import func
from quizproject import db
from quizproject.forms.answer_multi_form import MultipleValidAnswersForm
from quizproject.forms.answer_one_form import OneValidAnswerForm
from quizproject.models.answers import Answers

from quizproject.models.questions import Questions


main = Blueprint("main", __name__)


@main.route("/")
def index():
    return render_template("index.html")


@main.route("/profile")
@login_required
def profile():
    return render_template("profile.html", name=current_user.user_name)


# TODO: add tests to route
@main.route("/quiz")
@login_required
def quiz():
    # all questions have quiz id = 1
    # - currently there is only one quiz for roads
    question_number = db.session.query(func.count(Questions.question_id)).scalar()
    return render_template("quiz.html", question_number=question_number)


# TODO: add tests to route
@main.route("/quiz/viewer")
@login_required
def quiz_viewer():
    """get all questions with answers

    Returns:
       html: view for quiz
    """

    QUESTIONS_PER_PAGE = 1
    page = request.args.get("page", 1, type=int)
    questions = db.paginate(
        db.select(Questions),
        page=page,
        per_page=QUESTIONS_PER_PAGE,
    )

    # TODO: sanitize page arguments
    # TODO: validation arguments
    available_groups = db.session.query(Answers).filter(
        Answers.question_id == page)

    groups_list = [(i.answer_id, i.question_answer) for i in available_groups]

    multianswer = db.session.query(Questions.question_multianswer).filter(Questions.question_id == page)

    form1 = OneValidAnswerForm()
    form2 = MultipleValidAnswersForm()

    form1.user_answers.choices = groups_list
    form2.user_answers.choices = groups_list


    # parse to view
    return render_template("quiz-viewer.html",
                           questions=questions,
                           form1=form1,
                           form2=form2,
                           multianswer=multianswer)

# TODO: validate answers
# TODO: save answer when switch pages
# TODO: check answers
# TODO: redirect user to result page
