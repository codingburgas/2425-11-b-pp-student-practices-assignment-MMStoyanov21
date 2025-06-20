from flask import Blueprint, render_template, redirect, url_for, flash, session, current_app
from app import db, bcrypt
from flask_login import login_user, logout_user, current_user
from app.models import User
from app.auth.forms import RegistrationForm, LoginForm
from app.auth.utils import send_confirmation_email  # ✅ Import the email sender

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
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=hashed_pw,
            confirmed=False  # ✅ Make sure to set confirmed = False on creation
        )
        db.session.add(user)
        db.session.commit()

        send_confirmation_email(user.email)  # ✅ Send email confirmation
        flash('Account created! A confirmation email has been sent to you.', 'info')
        return redirect(url_for('auth.login'))

    return render_template('register.html', form=form)


@auth.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = LoginForm()
    if form.validate_on_submit():
        # Admin login
        if form.username.data == ADMIN_USERNAME and form.password.data == ADMIN_PASSWORD:
            session['is_admin'] = True
            session['admin_username'] = ADMIN_USERNAME
            flash('Admin logged in successfully.', 'success')
            return redirect(url_for('main.home'))

        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            if not user.confirmed:
                flash('Please confirm your email before logging in.', 'warning')  # ✅ Check confirmation
                return redirect(url_for('auth.login'))

            login_user(user, remember=form.remember.data)
            session['is_admin'] = False
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


@auth.route('/confirm/<token>')
def confirm_email(token):
    try:
        email = current_app.serializer.loads(token, salt='email-confirm', max_age=3600)
    except:
        flash('The confirmation link is invalid or has expired.', 'danger')
        return redirect(url_for('auth.login'))

    user = User.query.filter_by(email=email).first_or_404()
    if user.confirmed:
        flash('Account already confirmed. Please log in.', 'success')
    else:
        user.confirmed = True
        db.session.commit()
        flash('You have confirmed your account. Thanks!', 'success')

    return redirect(url_for('auth.login'))


@auth.route('/resend_confirmation')
def resend_confirmation():
    if current_user.is_authenticated and not current_user.confirmed:
        send_confirmation_email(current_user.email)
        flash('A new confirmation email has been sent.', 'info')
    return redirect(url_for('main.home'))
