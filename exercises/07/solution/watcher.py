#!/usr/bin/env python

import json
import os
import re
import requests
import subprocess
import time
import threading

import ansicolor

FINISHED_PLAYERS = set()


def app_request(player):
    r = requests.get(f'https://{player}-app.cloudapps.digital/version')
    if r.status_code == 200:
        try:
            version = json.loads(r.text)['version']
            if version == 2:
                config = subprocess.check_output(['cf', 'routes'], universal_newlines=True)
                config = ansicolor.strip_escapes(config)

                valid = False
                for line in config.split('\n'):
                    match = re.match(rf'^sandbox\s+{player}-app\s+cloudapps.digital\s+{player}-app$', line)
                    if match:
                        valid = True

                if valid:
                    requests.post(f'https://dmcf-leaderboard.cloudapps.digital/complete?exercise=7&player={player}')
                    FINISHED_PLAYERS.add(player)

        except:
            print(f'Failed parse version for {player}: {r.text}')
            FINISHED_PLAYERS.add(player)

    else:
        print(f'Failed request for {player}')


def watch_for_apps(players):
    while True:
        for player in players:
            t = threading.Thread(target=app_request, args=(player, ))
            t.setDaemon(True)
            t.start()

        time.sleep(2)
        for player in players:
            if player in FINISHED_PLAYERS:
                players.remove(player)

        if not players:
            break

    print('All done.')


if __name__ == '__main__':
    players = os.getenv('DMCF_USERS').split(',')
    watch_for_apps(players)
