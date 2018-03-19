## Solution for exercise 05
* `cd` into the `app` directory and use `cf push <INITIALS>-app -b staticfile_buildpack -i 2 -m 64M -k 64M -d cloudapps.digital -n <INITIALS>-app --health-check-type none`
* Use `cf delete-app <my_app_name>` to clean up your resources.


## Instructor notes
* Run ./watcher.py with DMCF_USERS set to the prefix for all participants to automatically monitor/report completion on the leaderboard. Ctrl+C out at the end of the exercise.
