from flask_wtf import FlaskForm
from wtforms import widgets, SelectMultipleField,  SubmitField

from wtforms.validators import DataRequired


class MultipleCheckBoxField(SelectMultipleField):
    """ Override class for SelectedMultiple field,

    Args:
        SelectMultipleField (FlaskForm): _description_
    """
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class MultipleValidAnswersForm(FlaskForm):
    """_summary_

    Args:
        FlaskForm (_type_): _description_
    """
    user_answers = MultipleCheckBoxField(
        "Label", coerce=int, choices=[], validators=[]
    )
    submit = SubmitField('Save')
