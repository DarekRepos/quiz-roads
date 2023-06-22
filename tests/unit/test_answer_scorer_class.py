import pytest
from unittest.mock import MagicMock

from quizproject.main.answer_scorer import AnswerScorer


@pytest.fixture
def session():
    return {
        "total_pages": 4,
        "answers": {1: ["A", "B"], 2: ["C"], 3: ["D", "E"], 4: []},
    }


@pytest.fixture
def db():
    return MagicMock()


def test_score_answers_all_correct_with_empty(session, db):
    """
    GIVEN
    4 questions
    WHEN
    - user select 1 valid question and leaves 3 empty questions
    - questions are multiple choice and single choice
    THEN
    - the user get score for 1 valid answers
    - empty answers are treated as a wrong answer and user don't get any points

    Args:
        session (_type_): session fixture
        db (_type_): database mock fixture
    """

    scorer = AnswerScorer(session, db)
    AnswerScorer.session = MagicMock(
        return_value={1: ["A", "B"], 2: []}
    )
    scorer._get_correct_answers = MagicMock(return_value=["A", "B"])
    percent = scorer.score_answers()
    assert percent == 25


# with muyltiple answers questions correct
def test_score_answers_all_correct_for_multiple_choice(session, db):
    """
    GIVEN
    4 questions
    WHEN
    - user select only 1 valid multiple choice question
    THEN
    - user get score for valid answer

    Args:
        session (_type_): session fixture
        db (_type_): database mock fixture
    """
    scorer = AnswerScorer(session, db)
    scorer._get_correct_answers = MagicMock(return_value=["A", "B"])
    percent = scorer.score_answers()
    assert percent == 25  # Assuming total_questions is 4


# with one question_answers
def test_score_answers_all_correct_for_single_choice(session, db):
    """
    GIVEN
    1 questions (from 4 available)
    WHEN
    - user select 1 valid single choice question
    THEN
    - user get score for valid answer

    Args:
        session (_type_): session fixture
        db (_type_): database mock fixture
    """
    scorer = AnswerScorer(session, db)
    scorer._get_correct_answers = MagicMock(return_value=["C"])
    percent = scorer.score_answers()
    assert percent == 25  # Assuming total_questions is 4


# user select not all answers with multiple questions
def test_score_answers_with_multiple_choice_incomplete(session, db):
    """
    GIVEN
    1 questions ( from 4 available) that have answer A and B
    WHEN
    - user did not mark all the correct answers for 1 multiple choice question
    THEN
    - user dont get any point for incomplete answers
    - incomplete answer is treated as a wrong answer



    Args:
        session (_type_): session fixture
        db (_type_): database mock fixture
    """
    scorer = AnswerScorer(session, db)
    scorer.session["answers"] = MagicMock(return_value=["A"])
    percent = scorer.score_answers()
    assert percent == 0  # Assuming total_questions is 4


def test_score_answers_none_correct(session, db):
    """
    GIVEN
    1 questions ( from 4 available)
    WHEN
    - all answers are incorrect for 1 multiple or single choice question
    THEN
    - user dont get any point

    Args:
        session (_type_): session fixture
        db (_type_): database mock fixture
    """
    scorer = AnswerScorer(session, db)
    scorer._get_correct_answers = MagicMock(return_value=["X", "Y"])
    percent = scorer.score_answers()
    assert percent == 0.0  # Assuming total_questions is 4


# get correct answer for  multiple questions
def test_get_correct_answers_with_multiple_choice(session, db):
    """
    GIVEN
    1 questions ( from 4 avaiable) with 4 answers
    it is multi choice question
    WHEN
    answer "A" and answer "B" are correct
    THEN
    return list with string that contain correct values "A" and "B"



    Args:
        session (_type_): session fixture
        db (_type_): database mock fixture
    """
    scorer = AnswerScorer(session, db)
    scorer.db.session.query().filter().all = MagicMock(
        return_value=[(1, "A"), (1, "B"), (0, "C"), (0, "D")]
    )
    correct_answers = scorer._get_correct_answers(1)
    assert correct_answers == ["A", "B"]


# test for one valid answers
def test_get_correct_answers_with_single_choice_answer(session, db):
    """
    GIVEN
    1 questions ( from 4 available) with 4 answers
    it is single choice question
    WHEN
    answer "C" is correct
    THEN
    return list with string that contain answer "C"


    Args:
        session (_type_): session fixture
        db (_type_): database mock fixture
    """
    scorer = AnswerScorer(session, db)
    scorer.db.session.query().filter().all = MagicMock(
        return_value=[(0, "A"), (0, "B"), (1, "C"), (0, "D")]
    )
    correct_answers = scorer._get_correct_answers(1)
    assert correct_answers == ["C"]
