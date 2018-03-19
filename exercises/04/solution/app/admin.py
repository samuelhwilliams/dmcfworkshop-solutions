from distutils.util import strtobool
import os

from flask import render_template, request, abort, current_app, flash
from flask.blueprints import Blueprint
from flask_nav.elements import Navbar, View

from .database import db
from .forms import CreateUserForm
from .models import User
from .nav import nav

admin = Blueprint('admin', __name__)

nav.register_element('admin_top',
                     Navbar(View('Home', 'main.home'),
                            View('Admin', 'admin.home'))
                     )

admin_path = os.getenv('ADMIN_URL_SLUG') if 'ADMIN_URL_SLUG' in os.environ.copy() else os.urandom(16).hex()
if admin_path.startswith('/'):
    admin_path = admin_path[1:]
if admin_path.endswith('/'):
    admin_path = admin_path[:-1]


@admin.route(f'/{admin_path}', methods=['GET', 'POST'])
def home():
    if not strtobool(os.getenv('ADMIN_ENABLED')):
        abort(403)

    create_user_form = None
    if current_app.config['SQLALCHEMY_DATABASE_URI'].startswith('postgres'):
        create_user_form = CreateUserForm()

    if request.method == 'POST' and create_user_form.validate_on_submit():
        db.create_all()
        if User.query.count() >= 1:
            flash('Sorry, the free version of this website only supports one user account. If you want to upgrade, '
                  'please give Sam lots of money.', 'warning')

        else:
            user = User(username=create_user_form.username.data, password=create_user_form.username.data)
            db.session.add(user)
            db.session.commit()

            flash(f'You have created a new account with username `{user.username}` and password `{user.password}`',
                  'success')

        return render_template('admin.html', form=CreateUserForm())

    return render_template('admin.html', form=create_user_form)
