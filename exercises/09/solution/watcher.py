#!/usr/bin/env python

# Steps:
# 1) Loop until / returns 200
# 2) Ssh onto box and delete app/templates/base.html
# 3) Loop until / returns 200
# 4) Hit /leak_memory endpoint every 2 seconds until endpoint returns non-200
# 5) Loop until / returns 200

import os
import requests
import threading

import pexpect

SUCCESSFUL_LOGIN_PATTERN = r'.+\[\d{2}\/Mar\/2018 \d{1,2}:\d{1,2}:\d{1,2}\] "GET \/logged_in HTTP\/1.1" 200.+'


def monitor_app_logs(player):
    global SUCCESSFUL_LOGIN_PATTERN

    print(f'Tailing logs for {player}-frontend; looking out for 200 on login ...')
    while True:
        try:
            c = pexpect.spawn(f'cf logs {player}-frontend')
            c.expect(SUCCESSFUL_LOGIN_PATTERN, timeout=None)
            requests.post(f'https://dmcf-leaderboard.cloudapps.digital/complete?exercise=9&player={player}')

        except:
            pass


if __name__ == '__main__':
    requests.post('https://dmcf-leaderboard.cloudapps.digital/start?exercise=9')

    players = os.getenv('DMCF_USERS').split(',')

    threads = []
    for player in players:
        t = threading.Thread(target=monitor_app_logs, args=(player,))
        t.setDaemon(True)
        t.start()
        threads.append(t)

    for t in threads:
        t.join()
