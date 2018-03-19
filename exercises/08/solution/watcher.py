#!/usr/bin/env python

# Steps:
# 1) Loop until / returns 200
# 2) Ssh onto box and delete app/templates/base.html
# 3) Loop until / returns 200
# 4) Hit /leak_memory endpoint every 2 seconds until endpoint returns non-200
# 5) Loop until / returns 200

import os
import random
import requests
import subprocess
import time
import threading


def mess_with_player(player):
    print(f'Monitoring for first 200 from {player}-app ...')
    res = requests.get(f'https://{player}-app.cloudapps.digital')
    while res.status_code != 200:
        res = requests.get(f'https://{player}-app.cloudapps.digital')
        time.sleep(5 + random.randint(1, 5))

    print(f'App up for {player} ...')
    time.sleep(20)

    print(f'Removing base template for {player} ...')
    while res.status_code != 500:
        subprocess.call(['cf', 'ssh', f'{player}-app', '-c', 'rm app/templates/base.html'])
        subprocess.call(['cf', 'ssh', f'{player}-app', '-c', 'echo "rm app/templates/base.html" >> .bash_history'])
        res = requests.get(f'https://{player}-app.cloudapps.digital')
        time.sleep(5)

    print(f'Template removed for {player} - waiting for recovery ...')
    while res.status_code != 200:
        res = requests.get(f'https://{player}-app.cloudapps.digital')
        time.sleep(5)

    print(f'App recovered for {player} - leaking memory ...')
    res_leak = res
    while res.status_code == res_leak.status_code or res_leak.status_code == 200 or res_leak.status_code == 502:
        res = requests.get(f'https://{player}-app.cloudapps.digital')
        res_leak = requests.get(f'https://{player}-app.cloudapps.digital/leak_memory')
        time.sleep(5)

    print(f'Waiting on recovery for {player} ...')
    while res.status_code != 200:
        res = requests.get(f'https://{player}-app.cloudapps.digital')
        time.sleep(5)

    print(f'App recovered for {player} - finished.')
    requests.post(f'https://dmcf-leaderboard.cloudapps.digital/complete?exercise=8&player={player}')


if __name__ == '__main__':
    players = os.getenv('DMCF_USERS').split(',')

    threads = []
    for player in players:
        t = threading.Thread(target=mess_with_player, args=(player,))
        t.setDaemon(True)
        t.start()
        threads.append(t)

    for t in threads:
        t.join()
