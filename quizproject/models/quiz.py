from .. import db


class Quiz(db.Model):
    __tablename__ = "quiz"
    quiz_id = db.Column(db.Integer, primary_key=True)
    quiz_name = db.Column(db.String(100), nullable=False)
    quiz_text = db.Column(db.String(100))
    quiz_idifficulty = db.Column(db.Integer)

    questions = db.relationship("Questions", back_populates="quiz")

    def __repr__(self) -> str:
        return f'<Quiz {self.quiz_name!r}>'

    def get_id(self):
        return (self.quiz_id)
