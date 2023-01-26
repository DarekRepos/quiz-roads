from quizproject.forms.baseform import MyBaseForm
from wtforms import BooleanField, PasswordField, SubmitField, StringField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from wtforms import ValidationError
from quizproject.models import User

class SignUpForm(MyBaseForm):
    username = StringField('Username',
            validators=[DataRequired(), Length(min=6, max=32)])
    email = StringField('Email',
            validators=[DataRequired(), Email(), Length(min=6, max=120)])
    password = PasswordField('Password',
            validators=[DataRequired(), Length(min=8, max=64)])
    confirm = PasswordField('Verify password',
            validators=[DataRequired(), EqualTo('password',
            message='Passwords must match')])