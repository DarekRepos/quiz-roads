import click

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
    try:
        question = Questions(
            quiz_id=2,
            question_dificulty=5,
            question_multianswer=1,
            question_text=name,
            is_active=1,
        )

        db.session.add(question)
        db.session.flush()
        # At this point, the object has been pushed to the DB,
        # and has been automatically assigned a unique primary key id

        id = question.get_id()

        answer1 = Answers(
            question_id=id, question_answer="test_answer 1", question_correct=1
        )
        answer2 = Answers(
            question_id=id, question_answer="test_answer 2", question_correct=0
        )
        answer3 = Answers(
            question_id=id, question_answer="test_answer 3", question_correct=0
        )
        answer4 = Answers(
            question_id=id, question_answer="test_ answer 4", question_correct=0
        )

        db.session.add(question)
        db.session.add(answer1)
        db.session.add(answer2)
        db.session.add(answer3)
        db.session.add(answer4)
        db.session.commit()

        click.echo("✅ Question {name} are created".format(name=name))

    except Exception:
    
        db.session.rollback()
        click.echo("Question did not created")


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


"""
remove items db
"""


@bp.cli.command("deleteall")
@with_appcontext
def deleteall():
    """
    Delete all examples questions and answers from database
    """
    message = 'Do you want to continue to delete all questions and answers?'
    click.confirm(message, abort=True)

    try:
        question_rows_deleted = db.session.query(Questions).delete()
        answer_rows_deleted = db.session.query(Answers).delete()
        db.session.commit()

    except Exception:
        db.session.rollback()

    click.echo(
        "total {questions} questions deleted with total {answers} answers deleted".format(
            questions=question_rows_deleted, answers=answer_rows_deleted
        )
    )
