import datetime

from flask_login import UserMixin
from .. import db


class User(UserMixin, db.Model):

    __tablename__ = "users"
    user_id = db.Column(db.Integer, primary_key=True)
    register_time = db.Column(
        db.DateTime, default=datetime.datetime.utcnow(), nullable=False)
    last_login = db.Column(
        db.DateTime, default=datetime.datetime.utcnow(), nullable=False)
    user_email = db.Column(db.String(100), unique=True, nullable=False)
    user_password = db.Column(db.String(100), nullable=False)
    user_name = db.Column(db.String(1000), unique=True, nullable=False)

    # participants = db.relationship('Participants', backref='users')

    def get_id(self):
        return (self.user_id)
