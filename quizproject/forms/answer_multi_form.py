from flask_wtf import FlaskForm
from wtforms import widgets, SelectMultipleField

from wtforms.validators import DataRequired


class MultipleCheckBoxField(SelectMultipleField):
    """ Overided class for SelectedMulitiple field, 

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
        "Label", coerce=int, choices=[], validators=[DataRequired()]
    )
