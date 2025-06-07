from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.survey.forms import ScoreForm, UploadCSVForm
from app.models import Survey, db
from app.ai_models.regression import LinearRegression
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64

survey = Blueprint('survey', __name__)


@survey.route("/predict", methods=["GET", "POST"])
@login_required
def predict():
    form = ScoreForm()
    if form.validate_on_submit():
        X = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        y = np.array([50, 55, 60, 65, 70, 75, 80, 85, 90, 95])
        model = LinearRegression()
        model.fit(X, y)
        predicted = model.predict(form.hours.data)

        entry = Survey(hours_studied=form.hours.data, predicted_score=predicted, author=current_user)
        db.session.add(entry)
        db.session.commit()

        return render_template("predict_result.html", score=predicted)
    return render_template("survey.html", form=form)


@survey.route("/upload", methods=["GET", "POST"])
@login_required
def upload_csv():
    form = UploadCSVForm()
    plot_url = None
    estimated_score = None

    if form.validate_on_submit():
        file = form.csv_file.data
        if file:
            try:
                df = pd.read_csv(file)

                if 'hours' not in df.columns:
                    flash("CSV must contain a 'hours' column.", 'danger')
                    return render_template("upload.html", form=form)

                # Generate a sequence of days
                df['days'] = range(1, len(df) + 1)

                X = df[['days']]
                y = df['hours']

                model = LinearRegression()
                model.fit(X.values.flatten(), y.values)

                # Predict score on next day (optional logic)
                next_day = [[len(df) + 1]]
                estimated_score = model.predict(next_day)[0]

                # Plotting
                plt.figure(figsize=(6, 4))
                plt.scatter(X, y, color='blue', label='Study Hours')
                plt.plot(X, model.predict(X.values.flatten()), color='red', label='Trend Line')
                plt.xlabel("Days")
                plt.ylabel("Hours Studied")
                plt.title("Study Trend and Estimation")
                plt.legend()

                buf = io.BytesIO()
                plt.savefig(buf, format='png')
                buf.seek(0)
                plot_url = base64.b64encode(buf.getvalue()).decode('utf8')
                buf.close()
                plt.close()

            except Exception as e:
                flash(f"Failed to process CSV: {e}", 'danger')

    return render_template("upload.html", form=form, plot_url=plot_url, estimated_score=estimated_score)
