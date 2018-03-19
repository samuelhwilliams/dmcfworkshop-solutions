import json
import os

from flask import render_template, url_for, redirect, request
from flask.blueprints import Blueprint
from flask_login import login_required, login_user, logout_user
from flask_nav.elements import Navbar, View
import requests

from .forms import LoginForm
from .nav import nav
from .login import login_manager
from .user import global_user


main = Blueprint('main', __name__)

nav.register_element('main_top',
                     Navbar(View('Home', '.home'), )
                     )


@login_manager.user_loader
def load_user(user_id):
    return global_user


@main.route('/', methods=['GET', 'POST'])
def home():
    login_form = LoginForm()

    if request.method == 'POST' and login_form.validate_on_submit():
        login_user(global_user)
        return redirect(url_for('.logged_in'))

    return render_template('home.html', form=login_form)


@main.route('/logged_in')
@login_required
def logged_in():
    try:
        player = json.loads(os.environ.get('VCAP_APPLICATION'))['application_name'].replace('-app', '')
        requests.post(f'https://dmcf-leaderboard.cloudapps.digital/complete?exercise=3&player={player}')

    except:
        pass

    logout_user()
    return render_template('logged_in.html')
