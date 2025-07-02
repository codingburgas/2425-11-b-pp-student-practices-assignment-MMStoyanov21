"""
Module: feedback/routes.py
Description: Blueprint to handle feedback submission and viewing.
"""

from flask import render_template, redirect, url_for, flash
from app.feedback import feedback
from app.feedback.forms import FeedbackForm
from flask_login import login_required, current_user
from app.models import Feedback
from app import db

@feedback.route('/feedback', methods=['GET', 'POST'])
@login_required
def feedback_form():
    """
    Display and process the feedback form for logged-in users.
    """
    form = FeedbackForm()
    feedbacks = Feedback.query.order_by(Feedback.timestamp.desc()).all()

    if form.validate_on_submit():
        new_feedback = Feedback(subject=form.subject.data,
                                message=form.message.data,
                                author=current_user)
        db.session.add(new_feedback)
        db.session.commit()
        flash('Thank you for your feedback!', 'success')
        return redirect(url_for('feedback.feedback_form'))

    return render_template('feedback.html', form=form, feedbacks=feedbacks)

@feedback.route('/feedback_view')
def view_feedback():
    """
    Public page to view anonymous feedback entries.
    """
    feedbacks = Feedback.query.order_by(Feedback.timestamp.desc()).all()
    return render_template('feedback.html', form=FeedbackForm(), feedbacks=feedbacks)
