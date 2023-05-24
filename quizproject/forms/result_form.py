from flask_wtf import FlaskForm
from wtforms import SubmitField


class ResultForm(FlaskForm):
    """_summary_

    Args:
        FlaskForm (_type_): _description_
    """

    submit = SubmitField("Complete Quiz & Check Yours Results")
