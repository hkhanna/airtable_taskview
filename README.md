# airtable_taskview
This tiny web app polls my Airtable todo list for tasks that have a certain field as true and returns a nice list of them with their status. Requires fields in the task table of `Name`, `Status`, `Created`. 

There are no dependencies other than the python3 standard library.

This script interacts with the following third-party services:
- Airtable

Logs go to `app.log` in the repo directory. 