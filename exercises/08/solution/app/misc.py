from flask import jsonify
from flask.blueprints import Blueprint


misc = Blueprint('misc', __name__)

MB = 1024 * 1024
MY_BIG_LEAK = ''
