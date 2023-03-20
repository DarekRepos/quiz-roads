from importlib.metadata import MetadataPathFinder
from .. import db

metadata = MetadataPathFinder()


class Answers(db.Model):
    __tablename__ = "answers",
    metadata,
    answer_id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.String(100), nullable=False)
    question_answer = db.Column(db.String(100))
    qquestion_correct = db.Column(db.Integer)

    questions = db.relationship('Questions', backref='quiz')

    def __repr__(self) -> str:
        return f'<Answer {self.question_answer}>'

    def get_id(self):
        return (self.answer_id)
