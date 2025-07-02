"""
Module: feedback/forms.py
Description: Defines the feedback submission form.
"""

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length

class FeedbackForm(FlaskForm):
    """
    Form for users to submit feedback messages.
    """
    subject = StringField('Subject', validators=[DataRequired(), Length(max=100)])
    message = TextAreaField('Message', validators=[DataRequired()])
    submit = SubmitField('Send Feedback')
