
from flask import render_template, flash, redirect, session, url_for, request, g
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db, lm
from .forms import LoginForm
from .models import User

import scrape_espn


@app.route('/')
@app.route('/index')
def index():
    user = g.user
    get_data = scrape_espn.get_data(week_num=2)
    get_data.run()

    upcoming_games = get_data.game_data[~get_data.game_data['game_complete']]
    completed_games = get_data.game_data[get_data.game_data['game_complete']]

    return render_template("index.html",
                           title='Home',
                           user=user,
                           tables=[upcoming_games.to_html(), completed_games.to_html()],
                           titles = ['na', 'Upcoming Games', 'Completed Games'])


@app.route('/login', methods=['GET', 'POST'])
def login():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(nickname=(form.user.data)).first()
        print user
        session['remember_me'] = form.remember_me.data
        remember_me = session['remember_me']
        session.pop('remember_me', None)
        login_user(user, remember=remember_me)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)


@lm.user_loader
def user_loader(id):
    return User.query.get(int(id))

@app.before_request
def before_request():
    g.user = current_user
