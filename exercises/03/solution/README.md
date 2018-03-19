## Solution for exercise 03
* Start the app with `cf start <my_app_name>`
* Get the login credentials from the app's environment with `cf env <my_app_name>` (though they're also shown in the output of `cf start`)
* Log into the app using those credentials.
* Use `cf delete-app <my_app_name>` to clear up your resources.
