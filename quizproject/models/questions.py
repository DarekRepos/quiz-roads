from .. import db


class Questions(db.Model):
    __tablename__ = "questions"
    question_id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey("quiz.quiz_id"))
    question_dificulty = db.Column(db.Integer, nullable=False)
    question_multianswer = db.Column(db.Integer, nullable=False)
    question_text = db.Column(db.String(1000))
    is_active = db.Column(db.Integer)

    quiz = db.relationship("Quiz", back_populates="questions")

    def __repr__(self):
        return f'<Question "{self.question_id!r}">'

    def get_id(self):

        return self.question_id
