from app import app
from flask import render_template, redirect, flash, url_for
from app.forms import LoginForm


@app.route('/')
@app.route('/index')
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


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    print(dir(form))
    return render_template('login.html', title='Sign In', form=form)