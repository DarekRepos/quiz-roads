import click

from quizproject.models.question_collection import QCollection

from ..models.quiz import Quiz
from .. import db
from ..models.questions import Questions
from ..models.answers import Answers


from flask import Blueprint, appcontext_popped, appcontext_pushed, current_app
from flask.cli import with_appcontext
import yaml

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
                question_text="Question 1",
                is_active=1,
            ),
            Questions(
                question_difficulty=5,
                question_multianswer=1,
                question_text="Question 2",
                is_active=1,
            ),
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
                question_text="Question 4",
                is_active=1,
            ),
            Questions(
                question_difficulty=5,
                question_multianswer=0,
                question_text="Question 5",
                is_active=1,
            ),
            Questions(
                question_difficulty=5,
                question_multianswer=0,
                question_text="Question 6",
                is_active=1,
            ),
            Questions(
                question_difficulty=5,
                question_multianswer=0,
                question_text="Question 7",
                is_active=1,
            ),
        ]

        db.session.add(roads)
        db.session.add(railway)
        db.session.flush()
        # At this point, the object has been pushed to the DB,
        # and has been automatically assigned a unique primary key id

        one = roads.get_item_by_name("Question 1")
        two = roads.get_item_by_name("Question 2")
        three = roads.get_item_by_name("Question 3")

        four = railway.get_item_by_name("Question 4")
        five = railway.get_item_by_name("Question 5")
        six = railway.get_item_by_name("Question 6")
        seven = railway.get_item_by_name("Question 7")

        # Create  test1 collection give name from the console
        test1 = QCollection(name=name, items=[one, two, three, four, five, six, seven])
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

        click.echo("✅ Questions collections {name} are created".format(name=name))

    except Exception as ex:
        db.session.rollback()
        click.echo("Question did not created")
        click.echo(ex)


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


@bp.cli.command("add_questions")
@with_appcontext
@click.option(
    "--file", type=click.Path(exists=True), help="Path to the YAML file", required=True
)
def add_questions(file):
    try:
        with open(file, "r") as f:
            questions = yaml.safe_load(f)

        # Process and validate each question
        processed_questions = []
        for question in questions:
            processed_question = process_question(question)
            processed_questions.append(processed_question)

        click.echo("Questions added successfully.")
    except FileNotFoundError:
        click.echo(f"File '{file}' not found.")
    except yaml.YAMLError as error:
        click.echo(f"Error parsing YAML file: {error}")


def process_question(question):
    # Get the question text and category
    question_text = question.get("question")
    category = question.get("category")

    # Process and validate the answers
    answers = question.get("answers", [])

    # For example, let's check if there are at least two correct answers
    correct_answers = [
        answer["answer"] for answer in answers if answer.get("is_correct")
    ]
    if len(correct_answers) > 1:
        current_app.logger.info(
            f"Warning: The question '{question_text}' in category '{category}' have at least two correct answers."
        )
        multianswer = 1
    else:
        multianswer = 0

    # question base variables
    # question_difficulty=5,
    # is_active=1,
    processed_question = Questions(
        question_text=question_text,
        question_difficulty=5,
        question_multianswer=multianswer,
        category=category,
        is_active=1,
    )
    db.session.add(processed_question)
    db.session.flush()
    for answer in answers:
        processed_answer = Answers(
            question_id=processed_question.question_id,
            question_answer=answer["answer"],
            question_correct=answer["is_correct"],
        )
        db.session.add(processed_answer)

    db.session.commit()
    # Return the processed question data
    return processed_question
