import json
import os

from flask import Flask
from flask_bootstrap import Bootstrap

from .database import db
from .main import main as main_blueprint
from .admin import admin as admin_blueprint
from .nav import nav
from .login import login_manager


def create_app():
    app = Flask(__name__)

    vcap_services = json.loads(os.getenv('VCAP_SERVICES', '{}'))
    database_uri = vcap_services.get('postgres', [{}])[0].get('credentials', {}).get('uri', 'sqlite:////tmp/no.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    login_manager.init_app(app)
    login_manager.login_view = 'main.home'
    login_manager.login_message_category = "must_login"

    Bootstrap(app)

    app.register_blueprint(main_blueprint)
    app.register_blueprint(admin_blueprint)

    app.config['BOOTSTRAP_SERVE_LOCAL'] = True
    app.config['SECRET_KEY'] = os.urandom(16).hex()

    nav.init_app(app)

    return app
