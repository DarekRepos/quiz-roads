
from flask_wtf import FlaskForm
# from quizproject.forms.baseform import MyBaseForm
from wtforms import BooleanField, PasswordField, SubmitField, EmailField, StringField
from wtforms.validators import InputRequired, Email, Length, DataRequired, EqualTo


class LoginForm(FlaskForm):
    email = EmailField('Email',
                       validators=[InputRequired(),
                                   Length(min=6, max=120), Email()])
    password = PasswordField('Password', validators=[InputRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Login')


class SignUpForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(),
                                       Length(min=6, max=32)])

    email = StringField('Email',
                        validators=[DataRequired(),
                                    Email(),
                                    Length(min=6, max=120)])

    password = PasswordField('Password',
                             validators=[DataRequired(),
                                         Length(min=8, max=64)])

    confirm = PasswordField('Verify password',
                            validators=[DataRequired(),
                                        EqualTo('password',
                                                message='Not match')])
