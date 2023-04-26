from .. import db

class PersonAnswer(db.Model):
    __tablename__ = "person_answers"
    person_answer_id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey("quiz.quiz_id"))
    question_id = db.Column(db.Integer, db.ForeignKey("question.question_id"))
    participant_id = db.Column(db.Integer,
                               db.ForeignKey("participants.participant_id"))
    answer_id = db.Column(db.Integer, db.ForeignKey("answers.answer_id"))
    question_time_start = db.Column(db.String(100), nullable=False)
    question_time_end = db.Column(db.String(100))

    # questions = db.relationship("Questions", backref="quiz")

    def __repr__(self) -> str:
        return f"<Quiz {self.person_answer_id }>"

    def get_id(self):
        return self.person_answer_id
