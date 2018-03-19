#!/usr/bin/env python

import os
import re
import requests
import subprocess
import time
import threading

import ansicolor


def watch_for_app(player):
    while True:
        r = requests.get(f'https://{player}-app.cloudapps.digital')
        if r.status_code != 200:
            time.sleep(5)
            continue

        try:
            config = subprocess.check_output(['cf', 'app', f'{player}-app'], universal_newlines=True)
            config = ansicolor.strip_escapes(config)

            instances, mem, disk, route_valid = None, None, None, False
            for line in config.split('\n'):
                match = re.match(r'^instances:\s+(\d)/(\d)$', line)
                if match:
                    instances = match.groups()[1]

                match = re.match(r'^#.+\s+(?:.+) of (.+)M\s+(?:.+) of (.+)M.+$', line)
                if match:
                    mem, disk = match.groups()

                match = re.match(r'^routes:\s+{player}-app\.cloudapps\.digital$'.format(player=player), line)
                if match:
                    route_valid = True

            if instances == '2' and mem == '64' and disk == '64' and route_valid:
                requests.post(f'https://dmcf-leaderboard.cloudapps.digital/complete?exercise=5&player={player}')
                break

        except:
            pass

        time.sleep(2)


def watch_for_apps(players):
    threads = []

    for player in players:
        t = threading.Thread(target=watch_for_app, args=(player, ))
        t.setDaemon(True)
        t.start()

        threads.append(t)

    for t in threads:
        t.join()


if __name__ == '__main__':
    players = os.getenv('DMCF_USERS').split(',')
    watch_for_apps(players)
