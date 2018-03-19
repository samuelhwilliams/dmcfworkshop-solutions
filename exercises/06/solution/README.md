## Solution for exercise 06
* Create the following `manifest.yml` file:
```Dockerfile
---
applications:
- name: <INITIALS>-app
  routes:
    - <INITIALS>-app.cloudapps.digital
  instances: 1
  memory: 128M
  disk_quota: 256M
  docker:
    image: digitalmarketplace/dmcfworkshop:exercise-06
  health-check-type: http
  health-check-http-endpoint: /_status
```
* Use `cf push <INITIALS>-app` to push your app using the manifest.
* Use `cf delete-app <my_app_name>` and `cf delete-service <my_service_name>` to clear up your resources.
