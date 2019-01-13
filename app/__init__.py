from flask import Flask

app = Flask(__name__)
# print(dir(app))

from app import routes
