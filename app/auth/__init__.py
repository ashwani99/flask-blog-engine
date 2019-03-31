from flask import Blueprint
from flask_login import LoginManager
from app import app

login = LoginManager(app)
login.login_view = 'auth.login'
bp = Blueprint('auth', __name__)

from app.auth import email, routes, forms