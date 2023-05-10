from flask_wtf import FlaskForm

# from quizproject.forms.baseform import MyBaseForm
from wtforms import RadioField
from wtforms.validators import DataRequired


class OneValidAnswerForm(FlaskForm):
    user_answers = RadioField("Label", coerce=int, choices=[], validators=[DataRequired()])
