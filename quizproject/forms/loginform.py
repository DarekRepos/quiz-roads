
from flask_wtf import FlaskForm as Form
from wtforms import BooleanField, PasswordField, SubmitField, EmailField
from wtforms.validators import  InputRequired, Email, Length
from quizproject.models import User


class LoginForm(Form):
    email = EmailField('Email',
            validators=[ InputRequired(), Length(min=6, max=120), Email()], 
            )
    password = PasswordField('Password', validators=[InputRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Login')
