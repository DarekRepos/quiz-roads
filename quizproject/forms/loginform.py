
from flask_wtf import FlaskForm as Form
from wtforms import BooleanField, PasswordField, SubmitField, StringField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from wtforms import ValidationError
from quizproject.models import User


class LoginForm(Form):
    email = StringField('Email',
            validators=[DataRequired(), Length(1, 64), Email()], 
            render_kw={'class':'input is-large','autofocus': True})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={'class':'input is-large'})
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Login')

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

    def validate(self):
        initial_validation = super(LoginForm, self).validate()
        if not initial_validation:
            return False
        user = User.query.filter_by(email=self.email.data).first()
        if not user:
            self.email.errors.append('Unknown email')
            return False
        if not user.verify_password(self.password.data):
            self.password.errors.append('Invalid password')
            return False
        return True