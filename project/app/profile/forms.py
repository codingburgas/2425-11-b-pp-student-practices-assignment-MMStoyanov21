"""
Module: profile/forms.py
Description: Defines forms for updating profile details.
"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo

class UpdateProfileForm(FlaskForm):
    """
    Form to update username and optionally password.
    """
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('New Password', validators=[Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[EqualTo('password')])
    submit = SubmitField('Update')
