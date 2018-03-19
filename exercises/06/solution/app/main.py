import json
import os
import re
import requests

from flask import render_template, jsonify
from flask.blueprints import Blueprint
from flask_nav.elements import Navbar, View

from .nav import nav


main = Blueprint('main', __name__)

nav.register_element('main_top',
                     Navbar(View('Home', '.home'), )
                     )


validated = False


def validate_config():
    global validated

    application = json.loads(os.environ.get('VCAP_APPLICATION'))

    player = application['application_name'].replace('-app', '')
    name_valid = re.match(r'^\w+-app$', application['application_name'])
    mem_valid = application['limits']['mem'] == 128
    disk_valid = application['limits']['disk'] == 256
    routes = application['application_uris']
    route_valid = any(route == f"{player}-app.cloudapps.digital" for route in routes)

    if name_valid and mem_valid and disk_valid and route_valid and not validated:
        req = requests.post(f'https://dmcf-leaderboard.cloudapps.digital/complete?exercise=6&player={player}')
        if req.status_code == 200:
            validated = True


@main.route('/')
def home():
    validate_config()
    return render_template('home.html', env=json.loads(os.environ.get('VCAP_APPLICATION')))


@main.route('/_status')
def status():
    validate_config()
    return jsonify({'status': 'OK'})
