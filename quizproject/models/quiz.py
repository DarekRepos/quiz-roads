from .. import db


class Quiz(db.Model):
    __tablename__ = "quiz"
    quiz_id = db.Column(db.Integer, primary_key=True)
    quiz_name = db.Column(db.String(100), nullable=False)
    quiz_text = db.Column(db.String(100))
    quiz_difficulty = db.Column(db.Integer)

    questions = db.relationship("Questions", back_populates="quiz")

    def __repr__(self) -> str:
        return f'<Quiz {self.quiz_name!r}>'

    def get_id(self):
        return (self.quiz_id)

    def get_item_by_name(self, item_name):
        """ In memory search for the item of this class of given name. """
        for item in self.questions:
            if item.question_text == item_name:
                return item
