from .. import db


class Questions(db.Model):
    __tablename__ = "questions"
    question_id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey("quiz.quiz_id"))
    question_difficulty = db.Column(db.Integer, nullable=False)
    question_multianswer = db.Column(db.Integer, nullable=False)
    question_text = db.Column(db.String(1000))
    category = db.Column(db.String(100))
    is_active = db.Column(db.Integer)

    quiz = db.relationship("Quiz", back_populates="questions")
    answers = db.relationship("Answers", back_populates="questions")

    def __repr__(self):
        return f'<Question "{self.question_id!r}">'

    def get_id(self):
        return self.question_id

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_all(items):
        return items.query.all()

    @classmethod
    def get_by_id(item, id):
        return item.query.get_or_404(id)
