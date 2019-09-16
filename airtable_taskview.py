import os
import sys
import json
from urllib import request, parse
from datetime import datetime as dt
import logging
import traceback

current_path = os.path.dirname(os.path.abspath(__file__))
logging.basicConfig(
    filename=current_path + "/app.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s - [%(name)s] %(message)s",
)
log = logging.getLogger("airtable_taskview")
log.info("Service started")

import env_vars
from bottle import route, run, template

# Uncaught Exception Logging
def uncaught_exception_handler(*exc_info):
    exc_text = "".join(traceback.format_exception(*exc_info))
    log.error("Uncaught exception: {}".format(exc_text))


sys.excepthook = uncaught_exception_handler


def isotimestamp(iso_string):
    return dt.strptime(iso_string, "%Y-%m-%dT%H:%M:%S.%fZ")


env_vars.load_file(current_path + "/.env")
host, port, airtable_base_id, airtable_key, airtable_table, airtable_field = env_vars.get_required(
    [
        "HOST",
        "PORT",
        "AIRTABLE_BASE_ID",
        "AIRTABLE_KEY",
        "AIRTABLE_TABLE",
        "AIRTABLE_FIELD",
    ]
)


@route("/")
def index():
    log.info("GET /")
    path_string = "/v0/{}/{}?filterByFormula={{{}}}&api_key={}".format(
        airtable_base_id,
        parse.quote(airtable_table),
        parse.quote(airtable_field),
        airtable_key,
    )
    res = request.urlopen("https://api.airtable.com" + path_string)

    records = json.loads(res.read().decode())["records"]
    if len(records) == 0:
        return "<pre>No tasks!</pre>"

    records = sorted(
        records, key=lambda x: isotimestamp(x["fields"]["Created"])
    )
    tasklist = []
    for task in records:
        if not task["fields"].get("Status"):
            status = "Backlog"
        else:
            status = task["fields"]["Status"]
        created_date = (
            isotimestamp(task["fields"]["Created"]).date().strftime("%m/%d/%Y")
        )

        tasklist.append(
            "- "
            + task["fields"]["Name"]
            + " <small>(created "
            + created_date
            + ")</small> / <strong>"
            + status
            + "</strong>"
        )

        if status == 'Done':
            tasklist[-1] = '<s>' + tasklist[-1] + '</s>'

    return_str = "<pre>Task List\n"
    return_str += "----------\n\n"
    return_str += "\n\n".join(tasklist)
    return_str += (
        "\n\n\n\n<i>completed tasks are periodically purged from this list</i>"
    )
    return_str += "</pre>"
    return return_str


run(host=host, port=port)
