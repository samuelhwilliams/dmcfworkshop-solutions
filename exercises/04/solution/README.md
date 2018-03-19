## Solution for exercise 04
* Check the app's environment with `cf env <my_app_name>`.
* Notice that the env variable ADMIN_ENABLED is set to false. Use `cf set-env` to turn it on.
* Notice that the env variable ADMIN_PATH is blank. Use `cf set-env` to give it a path.
* Restage the application so that environment variables are pulled in with `cf restage <my_app_name>`.
* Go to your admin URL and try to add a user. See an error that no (postgres) database is available.
  * See what services are available with `cf marketplace`.
  * Look at the plans available for postgres with `cf marketplace -s postgres`
  * Create a service instance with `cf create-service postgres free <my_service_name>`
  * Bind the service to your app with `cf bind-service <my_app_name> <my_service_name>`
  * Restage your app with `cf restage <my_app_name>`
* Go to the admin URL again and add a user.
* Login to the homepage with the created account.
* Use `cf delete-app <my_app_name>` and `cf delete-service <my_service_name>` to clear up your resources.
