import os
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user, logout_user
from werkzeug.utils import secure_filename
from app import db
from app.models import User, Upload, Estimation
from app.profile.forms import UpdateProfileForm

profile = Blueprint('profile', __name__)
UPLOAD_FOLDER = os.path.join('app', 'static', 'uploads')


@profile.route("/profile", methods=['GET', 'POST'])
@login_required
def view_profile():
    form = UpdateProfileForm(obj=current_user)

    if form.validate_on_submit():
        current_user.username = form.username.data

        if form.password.data:
            current_user.set_password(form.password.data)

        db.session.commit()
        flash('Profile updated successfully.', 'success')
        return redirect(url_for('profile.view_profile'))

    uploads = Upload.query.filter_by(user_id=current_user.id).order_by(Upload.timestamp.desc()).all()
    estimations = Estimation.query.filter_by(user_id=current_user.id).order_by(Estimation.timestamp.desc()).all()

    return render_template("profile.html", form=form, uploads=uploads, estimations=estimations)


@profile.route("/profile/upload", methods=['POST'])
@login_required
def upload_file():
    if 'file' not in request.files:
        flash('No file part in request.', 'danger')
        return redirect(url_for('profile.view_profile'))

    file = request.files['file']

    if file.filename == '':
        flash('No file selected.', 'warning')
        return redirect(url_for('profile.view_profile'))

    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)

        try:
            os.makedirs(UPLOAD_FOLDER, exist_ok=True)
            file.save(filepath)

            upload = Upload(filename=filename, user_id=current_user.id)
            db.session.add(upload)
            db.session.commit()

            flash('File uploaded successfully.', 'success')
        except Exception as e:
            flash(f'Error uploading file: {e}', 'danger')

    return redirect(url_for('profile.view_profile'))


@profile.route("/profile/delete", methods=['POST'])
@login_required
def delete_profile():
    user_id = current_user.id
    logout_user()
    user = User.query.get_or_404(user_id)

    uploads = Upload.query.filter_by(user_id=user_id).all()
    for upload in uploads:
        try:
            os.remove(os.path.join(UPLOAD_FOLDER, upload.filename))
        except Exception:
            pass

    db.session.delete(user)
    db.session.commit()

    flash('Your account has been deleted.', 'info')
    return redirect(url_for('main.home'))
