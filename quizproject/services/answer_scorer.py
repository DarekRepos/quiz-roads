from quizproject.models.answers import Answers


class AnswerScorer:
    """
    Encapsulate the functionality and data related
    to scoring the user's answers

    ...

    Attributes
    ----------
    session: list
    db: db object
    total_points: int
    total_questions: int

    Methods
    -------
    def score_answers()"
        return score for the answers ex. 33.33 it is value in %

    """

    def __init__(self, session, db):
        """
        Constructs all the necessary attributes for the person object.

        Args:
            session (_type_): flask session object
            db (_type_): flask database instance
        """
        self.session = session
        self.db = db
        self.total_points = 0
        self.total_questions = session["total_pages"]

    def score_answers(self) -> float:
        """
        Return percentage score from user answers

        Returns:
            float: Value is in percent [%] unit ex. 43.89
        """
        for item in range(1, self.total_questions + 1):
            try:
                user_answer = self.session["answers"][item]
            except KeyError as error:
                print(
                    f"I got a KeyError - reason:  empty answer for questions {str(error)} "
                )
                continue
            except:
                print("I got another exception, but I should re-raise")
                raise

            correct_answers = self._get_correct_answers(item)
            valid_answers = [x in user_answer for x in correct_answers]

            if all(valid_answers) and valid_answers:
                self.total_points += 1

        return round((self.total_points / self.total_questions) * 100, 2)

    def _get_correct_answers(self, question_id) -> list[str]:
        """
        Private method that get all correct answers
        for the selected id from database

        Args:
            question_id ( int ): it is from Questions. question_id
                it is id number for a question
        Returns:
            list[str]: it is a list with all correct answers
        """
        correct_answers = (
            self.db.session.query(Answers.question_correct, Answers.answer_id)
            .filter(Answers.question_id == question_id)
            .all()
        )
        correct_answers = [
            str(answer[1]) for answer in correct_answers if answer[0] == 1
        ]
        return correct_answers
