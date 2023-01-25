from flask_wtf import FlaskForm as Form
from wtforms import BooleanField, PasswordField, SubmitField, StringField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from wtforms import ValidationError
from quizproject.models import User

class SignUpForm(Form):
    username = StringField('Username',
            validators=[DataRequired(), Length(min=3, max=32)],
            render_kw={'class':'input is-large'})
    email = StringField('Email',
            validators=[DataRequired(), Email(), Length(min=6, max=40)],
            render_kw={'class':'input is-large'})
    password = PasswordField('Password',
            validators=[DataRequired(), Length(min=8, max=64)],
            render_kw={'class':'input is-large'})
    confirm = PasswordField('Verify password',
            validators=[DataRequired(), EqualTo('password',
            message='Passwords must match')],
            render_kw={'class':'input is-large'})

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

    def validate(self):
        initial_validation = super(SignUpForm, self).validate()
        if not initial_validation:
            return False
        user = User.query.filter_by(username=self.username.data).first()
        if user:
            self.username.errors.append("Username already registered")
            return False
        user = User.query.filter_by(email=self.email.data).first()
        if user:
            self.email.errors.append("Email already registered")
            return False
        return True