from importlib.metadata import MetadataPathFinder
from .. import db

metadata = MetadataPathFinder()


class Participants(db.Model):
    __tablename__ = "participants",
    metadata,
    participant_id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, primary_key=True)
    time_start = db.Column(db.String(100), nullable=False)
    time_end = db.Column(db.String(100))
    total_score = db.Column(db.Integer)

    questions = db.relationship('Questions', backref='quiz')

    def __repr__(self) -> str:
        return f'<Participant {self.participant_id}>'

    def get_id(self):
        return (self.participant_id)
