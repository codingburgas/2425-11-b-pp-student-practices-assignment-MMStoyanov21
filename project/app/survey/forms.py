from flask_wtf import FlaskForm
from wtforms import SubmitField
from flask_wtf.file import FileField, FileAllowed, FileRequired

class UploadCSVForm(FlaskForm):
    csv_file = FileField('Upload CSV File', validators=[
        FileRequired(message="CSV file is required."),
        FileAllowed(['csv'], 'CSV files only!')
    ])
    submit = SubmitField('Estimate From File')
