import os
import time

from flask import render_template, jsonify, request, abort
from flask.blueprints import Blueprint
from flask_nav.elements import Navbar, View

from .nav import nav
from .socketio import socket_io


main = Blueprint('main', __name__)

nav.register_element('main_top',
                     Navbar(View('Home', '.home'), )
                     )

NUM_EXERCISES = 9
players = os.environ.get('DMCF_USERS').split(',')
players_names = os.environ.get('DMCF_NAMES').split(',')
exercise_times = [{'start': 0, 'stop': 0} for x in range(1, NUM_EXERCISES+1)]
exercise_finishers = [{} for x in range(1, NUM_EXERCISES+1)]


@main.route('/')
def home():
    first_finishers = [min([y for y in x.items()], key=lambda z: z[1])[0] if x else [] for x in exercise_finishers]
    exercise_running_times = [
        (
            (int(time.time()) - x['start'])
            if x['start'] and not x['stop'] else
            (x['stop'] - x['start'])
            if x['start'] and x['stop'] else
            -1
            if x['stop'] else
            0
        ) for x in exercise_times
    ]

    return render_template('home.html',
                           players=players,
                           players_names=players_names,
                           first_finishers=first_finishers,
                           exercise_running_times=exercise_running_times,
                           exercise_finishers=exercise_finishers)


@main.route('/_status')
def status():
    return jsonify({'status': 'OK'})


@main.route('/<any(start, stop):action>', methods=['POST'])
def start_and_stop(action):
    exercise = int(request.args.get('exercise', 0))
    if not exercise:
        abort(400)

    action = action.lower()
    if not exercise_times[exercise - 1][action]:
        exercise_times[exercise - 1][action] = int(time.time())

    if action == 'stop':
        t = int(time.time())
        for player in players:
            if player not in exercise_finishers[exercise - 1]:
                start = exercise_times[exercise - 1]['start']
                exercise_finishers[exercise - 1][player] = 0 if not start else (t - start)

                socket_io.emit('complete',
                               {
                                   'exercise': exercise,
                                   'completed_by': exercise_finishers[exercise - 1],
                                   'completion_time': exercise_finishers[exercise - 1][player]
                               },
                               broadcast=True)

    socket_io.emit(action, {'exercise': exercise}, broadcast=True)

    return jsonify({'status': 'OK'})


@main.route('/complete', methods=['POST'])
def complete():
    player, exercise = request.args.get('player'), int(request.args.get('exercise', 0))
    if not player or not exercise:
        abort(400)

    if not exercise_times[exercise - 1]['start']:
        abort(400)

    t = int(time.time())
    if player not in exercise_finishers[exercise - 1]:
        exercise_finishers[exercise - 1][player] = t - exercise_times[exercise - 1]['start']

    socket_io.emit('complete',
                   {'exercise': exercise,
                    'completed_by': exercise_finishers[exercise - 1],
                    'completion_time': exercise_finishers[exercise - 1][player]},
                   broadcast=True)
    return jsonify({'status': 'OK'})
