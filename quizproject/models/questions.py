from importlib.metadata import MetadataPathFinder
from .. import db

metadata = MetadataPathFinder()


class Questions(db.Model):
    __tablename__ = "questions",
    metadata,
    question_id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.quiz_id'),
                        nullable=False)
    question_dificulty = db.Column(db.Integer, nullable=False)
    question_multianswer = db.Column(db.Integer, nullable=False)
    qustion_text = db.Column(db.String(1000))
    is_active = db.Column(db.Integer)

    answers = db.relationship('answers', backref='questions')

    def __repr__(self):
        return f'<Question "{self.question_id}">'

    def get_id(self):
        return (self.quiz_id)
