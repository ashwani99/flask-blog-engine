from app import app
from flask import render_template


@app.route('/')
def index():
    user = {'username': 'Ashwani'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Nothing useful to write here'
        },
        {
            'author': {'username': 'Shakespeare'},
            'body': 'What\'s in a name?'
        }
    ]
    return render_template('index.html', title='Home - Flask Blog Engine', user=user, posts=posts)