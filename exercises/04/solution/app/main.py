import json
import os

from flask import render_template, url_for, redirect, request, flash, current_app
from flask.blueprints import Blueprint
from flask_login import login_required, login_user, logout_user
from flask_nav.elements import Navbar, View
import requests

from .forms import LoginForm
from .models import User
from .nav import nav
from .login import login_manager


main = Blueprint('main', __name__)

nav.register_element('main_top',
                     Navbar(View('Home', 'main.home'), )
                     )


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@main.route('/', methods=['GET', 'POST'])
def home():
    login_form = LoginForm()

    if not current_app.config['SQLALCHEMY_DATABASE_URI'].startswith('postgres'):
        flash('No accounts are available at this time.', 'danger')

    else:
        if request.method == 'POST' and login_form.validate_on_submit():
            user = User.query.filter(User.username == login_form.username.data,
                                     User.password == login_form.password.data).first()

            if not user:
                flash('No account found with that username/password combination.', 'danger')

            else:
                login_user(user)
                return redirect(url_for('.logged_in'))

    return render_template('home.html', form=login_form)


@main.route('/logged_in')
@login_required
def logged_in():
    try:
        player = json.loads(os.environ.get('VCAP_APPLICATION'))['application_name'].replace('-app', '')
        requests.post(f'https://dmcf-leaderboard.cloudapps.digital/complete?exercise=4&player={player}')

    except:
        pass

    logout_user()
    return render_template('logged_in.html')
