import click

from quizproject.models.question_collection import QCollection

from ..models.quiz import Quiz
from .. import db
from ..models.questions import Questions
from ..models.answers import Answers


from flask import Blueprint, appcontext_popped, appcontext_pushed
from flask.cli import with_appcontext


bp = Blueprint("questions", __name__)
bp.cli.short_help = "Questions utilities"


@bp.cli.command("create")
@with_appcontext
@click.argument("name")
def create(name):
    """

    Added sample example tests questions

    """

    # Create two quiz categories
    roads = Quiz(quiz_name="Roads")
    railway = Quiz(quiz_name="Railway")

    try:
        roads.questions = [
            Questions(
                question_difficulty=5,
                question_multianswer=1,
                question_text="Question 3",
                is_active=1,
            ),
        ]

        railway.questions = [
            Questions(
                question_difficulty=5,
                question_multianswer=0,
                question_text="Question 1",
                is_active=1,
            ),
            Questions(
                question_difficulty=5,
                question_multianswer=0,
                question_text="Question 2",
                is_active=1,
            ),
        ]

        db.session.add(roads)
        db.session.add(railway)
        db.session.flush()
        # At this point, the object has been pushed to the DB,
        # and has been automatically assigned a unique primary key id

        three = roads.get_item_by_name("Question 3")
        two = railway.get_item_by_name("Question 2")
        one = railway.get_item_by_name("Question 1")

        # Create  test1 collection give name from the console
        test1 = QCollection(name=name, items=[one, two, three])
        db.session.add(test1)
        db.session.flush()

        # get all questions
        q = db.session.query(Questions).all()

        for item in q:
            # Create one answer with multiple solutions, check is 1
            if item.question_multianswer == 1:
                check = 1
            else:
                check = 0

            # Create  answers with one valid solution if check is 0
            answer1 = Answers(
                question_id=item.question_id,
                question_answer="test_answer 1",
                question_correct=1,
            )
            answer2 = Answers(
                question_id=item.question_id,
                question_answer="test_answer 2",
                question_correct=0,
            )
            answer3 = Answers(
                question_id=item.question_id,
                question_answer="test_answer 3",
                question_correct=0,
            )
            answer4 = Answers(
                question_id=item.question_id,
                question_answer="test_ answer 4",
                question_correct=check,
            )

            db.session.add(answer1)
            db.session.add(answer2)
            db.session.add(answer3)
            db.session.add(answer4)

        db.session.commit()

        click.echo("✅ Questions collections {name} are created".format(
            name=name))
        
    except Exception as e:
        db.session.rollback()
        click.echo("Question did not created")
        click.echo(e)


@bp.cli.command("count")
@with_appcontext
def question_count():
    """
    Count Questions and answers from database
    """

    counter_q = db.session.query(Questions).count()
    counter_a = db.session.query(Answers).count()

    click.echo(
        "total {questions} questions with total {answers} answers".format(
            questions=counter_q, answers=counter_a
        )
    )


@bp.cli.command("deleteall")
@with_appcontext
def deleteall():
    """
    Delete all examples questions and answers from database
    """
    message = "Do you want to continue to delete all questions and answers?"
    click.confirm(message, abort=True)

    try:
        question_rows_deleted = db.session.query(Questions).delete()
        answer_rows_deleted = db.session.query(Answers).delete()
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        click.echo(e)
    finally:
        click.echo(
            "total {q} questions and total {a} answers was deleted".format(
                q=question_rows_deleted, a=answer_rows_deleted
            )
        )
