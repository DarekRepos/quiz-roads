from flask_wtf import FlaskForm
from wtforms import widgets, SelectMultipleField, SubmitField, RadioField

# from quizproject.forms.baseform import MyBaseForm

from wtforms.validators import DataRequired


class OneValidAnswerForm(FlaskForm):
    """Form for one valid answer in radio fields"""

    user_answers = RadioField(
        "Label", coerce=int, choices=[], validators=[DataRequired()]
    )

    submit = SubmitField("Save")


class MultipleCheckBoxField(SelectMultipleField):

    """Override class for SelectedMultiple field"""

    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class MultipleValidAnswersForm(FlaskForm):
    """Form for multiple valid answers in checkboxes"""

    user_answers = MultipleCheckBoxField("Label", coerce=int, choices=[],
                                         validators=[])
    submit = SubmitField("Save")


class ResultForm(FlaskForm):
    """Result button that submit all answers and get score"""

    submit = SubmitField("Check Yours Results")
