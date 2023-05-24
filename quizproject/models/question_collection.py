from quizproject.models.questions import Questions
from .. import db


"""

"""
# this table contains many-to-many relationship
t_collection_item = db.Table(
    "q_collection_item",
    db.Model.metadata,
    db.Column("question_items_id",
              db.Integer,
              db.ForeignKey("questions.question_id"),
              primary_key=True),
    db.Column(
        "q_collections_id",
        db.Integer,
        db.ForeignKey("q_collections.id"),
        primary_key=True,
    ),
)


class QCollection(db.Model):
    __tablename__ = "q_collections"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    items = db.relationship(Questions,
                            secondary=t_collection_item,
                            backref="collections")
    
    def get_id(self):
        return self.question_id

