## Solution for exercise 08
* Try to visit the website in a browser and see it returns a 404.
* Check `cf logs` or `cf events` to see that the app instance isn't becoming healthy due to a failing healthcheck endpoint.
* Fix the healthcheck endpoint by returning a valid response (anything with a 200 HTTP status code)
* Fix the typo in the app manifest to point to the `/_status` rather than `/_stauts`
* Restarting at this stage will still not let the app come up. The status endpoint isn't returning anything. Add a response (eg `jsonify({"status": "ok"})`) to get it healthy again.
* After the app becomes healthy, the homepage will suddenly stop rendering correctly. `cf events <app>` will show that a developer ssh'd onto the box. `cf ssh <app>` will get you onto the instance,  where `history` will show what the dev did (deleted the base template for the app).
* `cf restart <app>` will re-deploy the existing droplet (with full source code) again, restoring the base template and the homepage will render again. Optionally, disable ssh with `cf disable-ssh <app>`.
* At this point the app will start to crash over time. `cf events`/`cf logs` will show requests to a leaky endpoint draining the instance's memory. Removing the leak and using `cf push` to update the app will bring the app back to full health.
