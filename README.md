# airtable_taskview
This tiny web app polls my Airtable todo list for tasks that have a certain field as true and returns a nice list of them with their status. Requires fields in the task table of `Name`, `Status`, `Created`. 

There are no dependencies other than the python3 standard library.

This script interacts with the following third-party services:
- Airtable

Logs go to `app.log` in the repo directory. 

## To Install on Debian VPS
- Clone the repo on your VPS
- Copy .env_example to .env and set the environment variables correctly.
  - If you're using a reverse proxy, the `HOST` should be set to `127.0.0.1`. Otherwise, you'll have to expose it to the internet with `HOST=0.0.0.0`.
- Install the service file in `/etc/systemd/system/airtable_taskview.service`. An `airtable_taskview.example.service` is included in this repo.
- Run `sudo systemctl start airtable_taskview`.
- Enable it at boot time `sudo systemctl enable airtable_taskview`.
- If you're using a reverse proxy like nginx, set up the appropriate rules in your `/etc/nginx/sites-enabled`.