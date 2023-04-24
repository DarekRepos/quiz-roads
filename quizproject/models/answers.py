from importlib.metadata import MetadataPathFinder
from .. import db

metadata = MetadataPathFinder()


class Answers(db.Model):
    __tablename__ = ("answers",)
    metadata,
    answer_id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(
        db.String(100), db.ForeignKey("question.question_id"), nullable=False
    )
    question_answer = db.Column(db.String(100))
    qquestion_correct = db.Column(db.Integer)

    questions = db.relationship("person_answers", backref="answers")

    def __repr__(self) -> str:
        return f"<Answer {self.question_answer}>"

    def get_id(self):
        return self.answer_id
