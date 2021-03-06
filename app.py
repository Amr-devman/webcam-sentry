from flask import Flask, redirect, url_for, render_template, request, jsonify, make_response
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.events import EVENT_JOB_ERROR, EVENT_JOB_EXECUTED
import atexit

import os
import random
import string
import logging

from utilities.db_functions import create_connection, create_creds_and_whitelist_tables
from utilities.housekeeping_functions import remove_old_data

app = Flask(__name__)

# comment this out if you want to see python print statements

log = logging.getLogger("werkzeug")
log.disabled = True

# we schedule a housekeeping function to run every hour, the task will remove
# old sqlite3 dbs if they exceed the 7 days data storage limit alloted for each user
# checks everyday
scheduler = BackgroundScheduler()
scheduler.add_job(func=remove_old_data , trigger="interval", seconds=60*60*24)
scheduler.start()

## kill the scheduled process when  the flask app is shutdown
atexit.register(lambda: scheduler.shutdown())

import sentry_setup_routes, sentry_run_routes

#create a cookie for new user and initialize a db for the user to data
@app.route('/', methods=["GET"])
def entry_page():
	if request.method =="GET":
		resp = make_response(redirect(url_for('setup_sentry')))

		if not request.cookies.get('userid'):
			userid = ''.join(random.choices(string.ascii_uppercase+string.digits,k=64))
			resp.set_cookie('userid', userid, max_age=60*60*24*7)
			create_connection(f"{userid}.db")
			create_creds_and_whitelist_tables(f"{userid}.db")
	return resp


if __name__ == '__main__':
	app.run(debug=True,host='0.0.0.0')
	if len(os.listdir("prev_images")) > 0:
		os.system("rm prev_images/*")

