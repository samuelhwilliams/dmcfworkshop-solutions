## Solution for exercise 09
* Create a database for your service with `cf create-service postgres Free <INITIALS>-app`
* Create a manifest as found alongside this readme.
* Deploy the apps using `cf push`
* Use `cf conduit <db_service_name> -- psql` to manually add a user to your database, or add it via the API with `curl -XPOST https://<INITIALS>-api.cloudapps.digital -d '{"user": {"username": "blah", "password": "blah", active: true}}' -h 'Content-Type: application/json'`
* Try to login to the frontend with the new user.
* When the app crashes, use `cf logs <INITIALS>-app --recent` to find the cause of the error.
* Correct the `json.loads(res)` to `json.loads(res.text)` in two places.
* Re-deploy the frontend using `cf push <INITIALS>-frontend`
* Login to finish.
