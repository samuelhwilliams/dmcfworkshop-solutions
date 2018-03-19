import json
import os

from flask import Flask

from .database import db
from .main import main as main_blueprint


def create_app():
    app = Flask(__name__)

    app.register_blueprint(main_blueprint)

    app.config['BOOTSTRAP_SERVE_LOCAL'] = True
    app.config['SECRET_KEY'] = os.urandom(16).hex()

    return app
