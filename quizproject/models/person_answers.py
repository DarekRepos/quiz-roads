from importlib.metadata import MetadataPathFinder
from .. import db

metadata = MetadataPathFinder()


class PeresonAnswers(db.Model):
    __tablename__ = "person_answers",
    metadata,
    person_answer_id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, primary_key=True)
    participant_id = db.Column(db.Integer, primary_key=True)    
    answer_id = db.Column(db.Integer, primary_key=True)    
    question_time_start = db.Column(db.String(100), nullable=False)
    question_time_end = db.Column(db.String(100))

    questions = db.relationship('Questions', backref='quiz')

    def __repr__(self) -> str:
        return f'<Quiz {self.person_answer_id }>'

    def get_id(self):
        return (self.person_answer_id)
