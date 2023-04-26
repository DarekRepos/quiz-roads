from .. import db


class Answers(db.Model):
    __tablename__ = "answers"
    answer_id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(
        db.Integer, db.ForeignKey("questions.question_id"), nullable=False
    )
    question_answer = db.Column(db.String(100))
    question_correct = db.Column(db.Integer)

    def __repr__(self) -> str:
        return f"<Answer {self.question_answer}>"

    def get_id(self):
        return self.answer_id
