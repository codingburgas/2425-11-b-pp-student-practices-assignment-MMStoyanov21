from flask_wtf import FlaskForm
from wtforms import FloatField, SubmitField
from wtforms.validators import DataRequired

class ScoreForm(FlaskForm):
    hours = FloatField('Hours Studied', validators=[DataRequired()])
    submit = SubmitField('Estimate Score')