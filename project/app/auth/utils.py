from flask import current_app, url_for
from flask_mail import Message
from app import mail  # ✅ mail is okay here


def send_confirmation_email(user_email):
    # ⬇️ Use serializer from the current Flask app context
    serializer = current_app.serializer

    token = serializer.dumps(user_email, salt='email-confirm')
    confirm_url = url_for('auth.confirm_email', token=token, _external=True)

    msg = Message('Confirm Your Email',
                  sender=current_app.config['MAIL_USERNAME'],
                  recipients=[user_email])
    msg.body = f"""Hi!

Click the link to confirm your email:
{confirm_url}

If you didn't register, just ignore this email."""

    mail.send(msg)
