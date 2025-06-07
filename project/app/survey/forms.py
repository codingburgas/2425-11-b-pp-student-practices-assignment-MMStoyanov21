from flask_wtf import FlaskForm
from wtforms import FloatField, SubmitField, FileField
from wtforms.validators import DataRequired, NumberRange
from flask_wtf.file import FileAllowed

class ScoreForm(FlaskForm):
    hours = FloatField('Hours Studied', validators=[
        DataRequired(), NumberRange(min=0, message="Hours must be positive")
    ])
    submit = SubmitField('Estimate Score')

class UploadCSVForm(FlaskForm):
    csv_file = FileField('Upload CSV File', validators=[
        DataRequired(), FileAllowed(['csv'], 'CSV files only!')
    ])
    submit = SubmitField('Estimate from File')
