## CloudFoundry workshop for the Digital Marketplace
A collection of exercises to accompany a Digital Marketplace CloudFoundry workshop.

## Presentation
http://tiny.cc/dmcfslides

## Solutions
Solutions to all of the exercises are included in the repository, including any setup required for the instructor. This area is probably under-documented, but essentially you need to set the variables DMCF_USERS and DMCF_NAMES. These are symmetrical lists of prefixes and full names (eg sw,kk,bv & Sam,Kev,Ben). The DMCF_USERS list of prefixes are used to create/track resources for the exercises. The full names are used in the display of the leaderboard app.

When you want to run an exercise, `cd` to the appropriate exercise's solution folder and run `./labs.sh setup`. If there's a `watcher.py` file alongside the labs script, run this after setup to automatically monitor participants' progress.

How to setup/teardown labs:
```bash
cd exercises/03
DMCF_USERS=sw,kk,gl DMCF_USERS_NAMES=Sam,Kev,George ./labs <setup|teardown>
./watcher.py  # if present
```
