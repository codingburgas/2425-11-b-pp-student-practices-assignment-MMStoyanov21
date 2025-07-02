"""
Module: survey/routes.py
Description: Route to handle CSV upload, run regression, and display result.
"""

import os
import io
import base64
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from flask import Blueprint, render_template, request, redirect, flash, url_for, current_app
from flask_login import login_required, current_user
from app.survey.forms import UploadCSVForm
from app.models import Survey
from app.ai_models.regression import LinearRegression
from app import db

survey = Blueprint('survey', __name__)

@survey.route("/predict", methods=["GET", "POST"])
@login_required
def predict():
    """
    Handle CSV upload, perform regression, save result, and display plot.
    """
    form = UploadCSVForm()
    plot_url = None

    if form.validate_on_submit():
        file = form.csv_file.data
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)

        try:
            df = pd.read_csv(filepath)
        except Exception as e:
            flash(f"Could not read CSV: {e}", "danger")
            return redirect(request.url)

        if 'hours' not in df.columns:
            flash("CSV must contain a 'hours' column", "danger")
            return redirect(request.url)

        hours = df['hours'].dropna().values
        if len(hours) == 0:
            flash("CSV has no valid 'hours' data", "danger")
            return redirect(request.url)

        days = np.arange(1, len(hours) + 1)
        model = LinearRegression()
        model.fit(days, hours)
        raw_pred = model.predict(np.array([len(hours) + 1]))[0]
        predicted = min(round(raw_pred * 30, 2), 100.0)

        entry = Survey(hours_studied=float(hours.mean()),
                       predicted_score=predicted,
                       author=current_user)
        db.session.add(entry)
        db.session.commit()

        plt.figure()
        plt.scatter(days, hours, color='blue', label='Observed')
        plt.plot(days, model.predict(days), color='red', label='Regression line')
        plt.xlabel("Day")
        plt.ylabel("Hours Studied")
        plt.title("Linear Regression from CSV")
        plt.legend()

        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        plot_url = f"data:image/png;base64,{base64.b64encode(buf.getvalue()).decode()}"
        plt.close()

        return render_template("predict_result.html", score=predicted, plot_url=plot_url)

    return render_template("survey.html", upload_form=form)
