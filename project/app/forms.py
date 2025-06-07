from flask_wtf import FlaskForm
from wtforms import FloatField, SubmitField,StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length, EqualTo, Email


class ScoreForm(FlaskForm):
    hours = FloatField('Hours Studied', validators=[DataRequired()])
    submit = SubmitField('Estimate Score')
class EditProfileForm(FlaskForm):
    username = StringField('New Username', validators=[Length(min=2, max=20)])
    email = StringField('New Email', validators=[Email()])
    submit = SubmitField('Update Profile')

class RequestPasswordResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('New Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')

class DeleteAccountForm(FlaskForm):
    submit = SubmitField('Delete Account')