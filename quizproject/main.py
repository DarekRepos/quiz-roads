from flask import Blueprint, redirect, render_template, request, session, url_for

from flask_login import login_required, current_user
from sqlalchemy import func
from quizproject import db
from quizproject.forms.answer_multi_form import MultipleValidAnswersForm
from quizproject.forms.answer_one_form import OneValidAnswerForm

from quizproject.forms.result_form import ResultForm

from quizproject.models.answers import Answers
from quizproject.models.question_collection import QCollection

from quizproject.models.questions import Questions
from quizproject.models.quiz import Quiz


main = Blueprint("main", __name__)
QUESTIONS_PER_PAGE = 1


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
    question_number = db.session.query(func.count(Questions.question_id)).scalar()
    return render_template("quiz.html", question_number=question_number)


# TODO: add tests to route


@main.route("/quiz/viewer", methods=["GET", "POST"])
@login_required
def quiz_viewer():
    """get all questions with answers

    Returns:
       html: view for quiz
    """
    session["checked"] = "checked"

    page = request.args.get("page", 1, type=int)

    # get collections which has "Raods" question

    questions = db.paginate(
        db.session.query(QCollection)
        .join(Questions, QCollection.items)
        .filter(QCollection.id == 1),
        page=page,
        per_page=QUESTIONS_PER_PAGE,
    )
    for coll in questions:
        print(coll)
        for item in coll.items:
            print(item.question_text)

    # TODO: sanitize page arguments
    # TODO: validation arguments

    available_groups = db.session.query(Answers).filter(Answers.question_id == page)

    groups_list = [(i.answer_id, i.question_answer) for i in available_groups]

    multianswer = db.session.query(Questions.question_multianswer).filter(
        Questions.question_id == page
    )

    form1 = OneValidAnswerForm(request.form)
    form2 = MultipleValidAnswersForm(request.form.getlist("user_answers"))
    form3 = ResultForm(request.form)

    form1.user_answers.choices = groups_list
    form2.user_answers.choices = groups_list

    pages = questions.pages

    session["total_pages"] = pages
    session["current_question"] = [page]

    selections = []

    if "answers" in session:
        if page in session["answers"]:
            selections = session["answers"][page]
        else:
            session["answers"][page] = []
    else:
        session["answers"] = {page: []}

    session.modified = True

    # if next display view with nezt questions
    if form2.validate_on_submit() and (request.method == "POST"):
        op1 = request.form.getlist("user_answers")
        user_answers = dict(groups_list)

        for key in user_answers:
            for answer_item in op1:
                if int(answer_item) == key:
                    if "answers" in session and page in session["answers"]:
                        session["answers"][page] = op1
                    else:
                        session["answers"] = {page: [op1]}
        return redirect(url_for(
            "main.quiz_viewer", page=page, selections=selections))

    if form1.validate_on_submit() and (request.method == "POST"):
        return redirect(url_for(
            "main.quiz_viewer", page=page, selections=selections))
    # parse to view
    return render_template(
        "quiz-viewer.html",
        questions=questions,
        form1=form1,
        form2=form2,
        form3=form3,
        selections=selections,
        multianswer=multianswer,
    )


@main.route("/results", methods=["POST"])
@login_required
def results():
    print(session["total_pages"])

    points = 0
    correct = False
    count = 0
    valid = 0
    total_questions = session["total_pages"]

    for item in range(1, session["total_pages"] + 1):
        print("wszystkie", session["answers"][item])
        answers = db.session.query(Answers.answer_id, Answers.question_correct).filter(
            Answers.question_id == item
        )

        # TODO: fix result page
        # TODO: Refactor to class based 
        for a, b in answers:
            for k in session["answers"][item]:
                # question have multiple answers
                if len(k) > 1:
                    for v in k:
                        if int(b) == 1:
                            count = count + 1
                        if int(v) == int(a):
                            if int(b) == 1:
                                valid = valid + 1
                                correct = True
                            print("OK")
                if correct is True and count == valid:
                    points = points + 1
                else:
                    print(k[0])
                    if int(k[0]) == a:
                        if int(b) == 1:
                            points = points + 1

                print(a, " i ", b, " i ")

    procent = round((points / total_questions) * 100)
    return render_template(
        "result.html", points=points, total_questions=total_questions, procent=procent
    )


# TODO: validate answers
