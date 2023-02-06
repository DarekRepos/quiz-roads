# from quizproject.forms.baseform import MyBaseForm
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField
from wtforms.validators import DataRequired, Email, EqualTo, Length


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
