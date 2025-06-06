from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.survey.forms import ScoreForm
from app.models import Survey, db
from app.ai_models.regression import LinearRegression
import numpy as np

survey = Blueprint('survey', __name__)

@survey.route("/predict", methods=["GET", "POST"])
@login_required
def predict():
    form = ScoreForm()
    if form.validate_on_submit():
        X = np.array([1,2,3,4,5,6,7,8,9,10])
        y = np.array([50,55,60,65,70,75,80,85,90,95])
        model = LinearRegression()
        model.fit(X, y)
        predicted = model.predict(form.hours.data)

        entry = Survey(hours_studied=form.hours.data, predicted_score=predicted, author=current_user)
        db.session.add(entry)
        db.session.commit()

        return render_template("predict_result.html", score=predicted)
    return render_template("survey.html", form=form)
