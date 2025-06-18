from flask import Blueprint, render_template, redirect, url_for, flash, session
from app import db, bcrypt
from flask_login import login_user, logout_user, current_user
from app.models import User
from app.auth.forms import RegistrationForm, LoginForm

auth = Blueprint('auth', __name__)

# Admin credentials (hardcoded)
ADMIN_USERNAME = "admin01"
ADMIN_PASSWORD = "admin_acc"

@auth.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You can now log in.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('register.html', form=form)

@auth.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        # Check if admin login
        if form.username.data == ADMIN_USERNAME and form.password.data == ADMIN_PASSWORD:
            # Mark admin logged in using session
            session['is_admin'] = True
            session['admin_username'] = ADMIN_USERNAME
            flash('Admin logged in successfully.', 'success')
            return redirect(url_for('main.home'))

        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            session['is_admin'] = False  # Normal user
            return redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', form=form)

@auth.route("/logout")
def logout():
    logout_user()
    session.pop('is_admin', None)
    session.pop('admin_username', None)
    return redirect(url_for('main.home'))
