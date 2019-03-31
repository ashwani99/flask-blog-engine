from flask import render_template
from flask_mail import Message
from app import app, mail
from threading import Thread


def send_password_reset_email(user):
    token = user.get_reset_password_token()
    send_email('[Flask Blog Engine] Reset Your Password',
                sender=app.config['ADMINS'][0],
                recipients=[user.email],
                text_body=render_template('email/reset_password.txt',
                                        user=user, token=token),
                html_body=render_template('email/reset_password.html',
                                        user=user, token=token))