from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo


class UpdateProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])

    password = PasswordField('New Password', validators=[
        Length(min=6, message="Password must be at least 6 characters"),
    ])

    confirm_password = PasswordField('Confirm Password', validators=[
        EqualTo('password', message='Passwords must match')
    ])

    submit = SubmitField('Update')
