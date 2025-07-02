"""
Module: forms.py
Description: Miscellaneous forms for scoring, profile edits, password reset, etc.
"""

from flask_wtf import FlaskForm
from wtforms import FloatField, StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, Email

class ScoreForm(FlaskForm):
    """
    Form to estimate score based on hours studied.
    """
    hours = FloatField('Hours Studied', validators=[DataRequired()])
    submit = SubmitField('Estimate Score')

class EditProfileForm(FlaskForm):
    """
    Form to edit username and/or email.
    """
    username = StringField('New Username', validators=[Length(min=2, max=20)])
    email = StringField('New Email', validators=[Email()])
    submit = SubmitField('Update Profile')

class RequestPasswordResetForm(FlaskForm):
    """
    Form for requesting a password reset via email.
    """
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

class ResetPasswordForm(FlaskForm):
    """
    Form for entering a new password and confirmation.
    """
    password = PasswordField('New Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')

class DeleteAccountForm(FlaskForm):
    """
    Simple form for account deletion confirmation.
    """
    submit = SubmitField('Delete Account')
