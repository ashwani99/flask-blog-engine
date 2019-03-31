from flask import Blueprint
from flask_login import LoginManager
from app import app

bp = Blueprint('auth', __name__)

from app.auth import email, routes, forms