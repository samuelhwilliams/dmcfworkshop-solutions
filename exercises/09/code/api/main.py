import os
import math
from flask import jsonify, abort
from flask.blueprints import Blueprint

from .models import User


main = Blueprint('main', __name__)


@main.route('/')
def home():
    return jsonify({"status": "ok"})


@main.route('/users')
def users():
    return jsonify({'users': [user.serialize() for user in User.query.all()]})


@main.route('/users/<int:user_id>')
def get_user_by_id(user_id):
    user = User.query.get(user_id)
    if not user:
        abort(404)

    return jsonify({'user': user.serialize()})


@main.route('/users/<string:username>')
def get_user_by_username(username):
    return jsonify({'user': User.query.filter(User.username == username).first_or_404().serialize()})


def get_disk_space_status(low_disk_percent_threshold=5):
    """Accepts a single parameter that indicates the minimum percentage of disk space which should be free for the
    instance to be considered healthy.

    Returns a tuple containing two items: a status (OK or LOW) indicating whether the disk space remaining on the
    instance is below the threshold and the integer percentage remaining disk space."""
    disk_stats = os.statvfs('/')

    disk_free_percent = int(math.ceil(((disk_stats.f_bfree * 1.0) / disk_stats.f_blocks) * 100))

    return 'OK' if disk_free_percent >= low_disk_percent_threshold else 'LOW', disk_free_percent


@main.route('/_status')
def status():
    disk_status=get_disk_space_status()
    return jsonify({"status": "ok" if disk_status[0] == 'OK' else 'error', 'disk': disk_status[1]}), 200 if disk_status[1] >= 5 else 500
