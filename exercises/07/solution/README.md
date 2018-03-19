## Solution for exercise 06
* `cd app` and edit `manifest.yml` to have your personal (temporary) app name.
* `cf push` the app
* `cf map-route <tmp-app-name> cloudapps.digital -n <INITIALS>-app` to load balance requests across both the new and old apps
* `cf unmap-route <old-app-name> cloudapps.digital -n <INITIALS>-app` to remove the old app from the load balancer
* Wait for existing requests to have been processed (60 seconds)
* `cf delete <old-app-name>` to remove the old app altogether
* `cf rename <new-app-name> <old-app-name>` to switch the app names across.
* `cf unmap-route` for any auto assigned routes on the new app, unless you specified to assign no route when pushing.
